import unicodedata
from difflib import get_close_matches

import networkx as nx
import pandas as pd

LINEAGE_COLORS = [
    "#E9A227", "#AEBDCA", "#4DB7B3", "#E76F51", "#8E7DBE",
    "#6BCB77", "#4A9EFF", "#FF6B9D", "#C9B037", "#B0714C",
]
POTION_COLOR = "#555B66"
MATCH_CUTOFF = 0.85


def _key(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text).lower())
    return "".join(c for c in text if c.isalpha())


def load_network_data(workbook_path="data/potions-craft.xlsx"):
    return (
        pd.read_excel(workbook_path, sheet_name="potions-inventeurs"),
        pd.read_excel(workbook_path, sheet_name="liste-inventeurs"),
    )


def build_inventor_reference(inventors: pd.DataFrame) -> dict:
    reference = {}
    for _, row in inventors.iterrows():
        name = f"{row['pseudo']} {row['lignee']}".strip()
        reference[_key(name)] = (name, str(row["lignee"]).strip())
    return reference


def resolve_inventor(raw, reference: dict):
    """Rattache une orthographe au nom canonique. None si vide ou inconnu."""
    if pd.isna(raw) or not str(raw).strip():
        return None
    key = _key(raw)
    if key in reference:
        return reference[key][0]
    close = get_close_matches(key, reference.keys(), n=1, cutoff=MATCH_CUTOFF)
    return reference[close[0]][0] if close else None


def build_graph(potions: pd.DataFrame, inventors: pd.DataFrame) -> nx.Graph:
    """Noeuds inventeur (couleur = lignee, taille = nb de potions) et potion.

    Choix assume : une potion sans inventeur connu reste dans le graphe
    comme noeud isole (sans arete), au lieu d'etre reliee a un faux
    inventeur "Inconnu" qui laisserait croire a un lien reel.
    """
    reference = build_inventor_reference(inventors)
    lineages = sorted({lineage for _, lineage in reference.values()})
    lineage_colors = {
        lin: LINEAGE_COLORS[i % len(LINEAGE_COLORS)] for i, lin in enumerate(lineages)
    }
    lineage_of = {name: lin for name, lin in reference.values()}

    graph = nx.Graph()
    potions = potions.drop_duplicates(subset="potion")
    resolved = potions["inventeur"].apply(lambda v: resolve_inventor(v, reference))
    counts = resolved.value_counts()

    for name, lineage in lineage_of.items():
        n = int(counts.get(name, 0))
        graph.add_node(
            name, kind="inventor", label=name, lineage=lineage,
            potions=n, size=14 + 5 * n, color=lineage_colors[lineage],
        )

    for potion, inventor in zip(potions["potion"], resolved):
        inventor = None if pd.isna(inventor) else inventor  # apply() transforme None en NaN
        graph.add_node(
            potion, kind="potion", label=potion, size=8, color=POTION_COLOR,
            inventor=inventor or "Unknown",
        )
        if inventor:
            graph.add_edge(inventor, potion)

    graph.graph["lineage_colors"] = lineage_colors
    return graph


def build_anomaly_report(potions: pd.DataFrame, inventors: pd.DataFrame) -> pd.DataFrame:
    """Orthographes rapprochees automatiquement et potions sans inventeur."""
    reference = build_inventor_reference(inventors)
    rows = []
    for _, row in potions.iterrows():
        raw = row["inventeur"]
        resolved = resolve_inventor(raw, reference)
        if pd.isna(raw):
            rows.append((row["potion"], "", "", "inventeur manquant : noeud isole"))
        elif resolved is None:
            rows.append((row["potion"], raw, "", "inventeur inconnu : noeud isole"))
        elif resolved != raw:
            rows.append((row["potion"], raw, resolved, "orthographe rapprochee"))
    return pd.DataFrame(rows, columns=["potion", "valeur", "rapprochee_de", "decision"])