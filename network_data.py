import re
import pandas as pd
import networkx as nx


def normaliser(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zàâäçéèêëîïôöùûüÿñ -]", "", text)
    return text


def normalize_column(df, column_name, default_value="unknown"):
    df = df.copy()
    df[column_name] = df[column_name].apply(normaliser)
    df[column_name] = df[column_name].fillna(default_value)
    return df


def format_name(value):
    if pd.isna(value):
        return value
    return str(value).title()


COL_POTION = "potion"
COL_INVENTOR_IN_POTIONS_SHEET = "inventeur"
COL_PSEUDO = "pseudo"
COL_LINEAGE = "lignee"

DEFAULT_COLOR = "#888888"
LINEAGE_COLORS = ["#e9a227", "#aebdca", "#4db7b3", "#e76f51", "#8e7dbe"]


def load_data(excel_path):
    potions = pd.read_excel(excel_path, sheet_name="potions-inventeurs")
    inventors = pd.read_excel(excel_path, sheet_name="liste-inventeurs")
    return potions, inventors


def clean_data(potions, inventors):
    potions = normalize_column(potions, COL_INVENTOR_IN_POTIONS_SHEET, default_value="unknown")
    potions = normalize_column(potions, COL_POTION, default_value="unknown potion")
    inventors = normalize_column(inventors, COL_PSEUDO)
    inventors = normalize_column(inventors, COL_LINEAGE)
    return potions, inventors


def count_potions_by_inventor(potions):
    return potions[COL_INVENTOR_IN_POTIONS_SHEET].value_counts().to_dict()


def build_inventor_name(pseudo, lineage):
    return f"{pseudo} {lineage}"


def get_lineage_by_inventor(inventors):
    result = {}
    for _, row in inventors.iterrows():
        full_name = build_inventor_name(row[COL_PSEUDO], row[COL_LINEAGE])
        result[full_name] = row[COL_LINEAGE]
    return result


def build_lineage_colors(inventors):
    lineages = sorted(inventors[COL_LINEAGE].dropna().unique())
    return {
        lineage: LINEAGE_COLORS[index % len(LINEAGE_COLORS)]
        for index, lineage in enumerate(lineages)
    }


def build_graph(potions, inventors):
    graph = nx.Graph()

    potion_counts = count_potions_by_inventor(potions)
    lineages = get_lineage_by_inventor(inventors)
    lineage_colors = build_lineage_colors(inventors)

    for inventor_name, potion_count in potion_counts.items():
        lineage = lineages.get(inventor_name) or inventor_name.rsplit(" ", 1)[-1]
        if lineage not in lineage_colors:
            lineage_colors[lineage] = LINEAGE_COLORS[
                len(lineage_colors) % len(LINEAGE_COLORS)
            ]

        graph.add_node(
            inventor_name,
            node_type="inventor",
            label=format_name(inventor_name),
            lineage=lineage,
            size=20 + potion_count * 8,
            color=lineage_colors[lineage],
        )

    for _, row in potions.iterrows():
        potion_name = row[COL_POTION]
        inventor_name = row[COL_INVENTOR_IN_POTIONS_SHEET]

        if potion_name not in graph:
            graph.add_node(
                potion_name,
                node_type="potion",
                label=format_name(potion_name),
                size=10,
                color="#555555",
            )

        if inventor_name not in graph:
            graph.add_node(
                inventor_name,
                node_type="inventor",
                label=format_name(inventor_name),
                size=15,
                color=DEFAULT_COLOR,
            )

        graph.add_edge(inventor_name, potion_name)

    graph.graph["lineage_colors"] = lineage_colors
    return graph


if __name__ == "__main__":
    potions, inventors = load_data("data/potions-craft.xlsx")

    potions, inventors = clean_data(potions, inventors)

    print("Unique inventors after cleaning:")
    print(potions[COL_INVENTOR_IN_POTIONS_SHEET].value_counts())

    print()
    print("Noms reconstruits depuis liste-inventeurs:")
    print(list(get_lineage_by_inventor(inventors).keys()))

    graph = build_graph(potions, inventors)

    print()
    print(f"Total nodes: {graph.number_of_nodes()}")
    print(f"Total edges: {graph.number_of_edges()}")