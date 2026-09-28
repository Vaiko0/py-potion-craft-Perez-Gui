# potions_magic_type.py
import pandas as pd


def load_magic_type_data(workbook_path="data/potions-craft.xlsx"):
    """Charge les feuilles necessaires au sunburst."""
    return (
        pd.read_excel(workbook_path, sheet_name="liste-types-de-magie"),
        pd.read_excel(workbook_path, sheet_name="potions-inventeurs"),
    )


def build_sunburst_data(
    magic_types: pd.DataFrame, potions_inventeurs: pd.DataFrame
) -> pd.DataFrame:
    """Construit ids/labels/parents/values pour le sunburst.

    Aucun lien potion <-> competence n'existe dans le classeur : les potions
    d'un type sont reparties a tour de role entre les competences de ce type.
    Chaque potion apparait donc une seule fois (60 secteurs pour 60 potions).
    """
    ids, labels, parents, values = [], [], [], []

    competences_par_type = {
        row["type_de_magie"]: [
            c.strip() for c in str(row["competences"]).split(";") if c.strip()
        ]
        for _, row in magic_types.iterrows()
    }

    # niveau 1 : types de magie
    for type_magie in competences_par_type:
        ids.append(f"type::{type_magie}")
        labels.append(type_magie)
        parents.append("")
        values.append(0)

    # niveau 2 : competences (une instance par type qui la mobilise)
    for type_magie, competences in competences_par_type.items():
        for competence in competences:
            ids.append(f"competence::{type_magie}::{competence}")
            labels.append(competence)
            parents.append(f"type::{type_magie}")
            values.append(0)

    # niveau 3 : potions, reparties a tour de role, une seule fois chacune
    compteur_par_type = {type_magie: 0 for type_magie in competences_par_type}
    potions_uniques = potions_inventeurs.drop_duplicates(subset="potion")

    for _, potion in potions_uniques.iterrows():
        type_magie = potion["type-magie-potion"]
        competences = competences_par_type.get(type_magie)
        if not competences:
            continue  # type de magie inconnu : potion ecartee

        index = compteur_par_type[type_magie]
        competence = competences[index % len(competences)]
        compteur_par_type[type_magie] += 1

        ids.append(f"potion::{type_magie}::{competence}::{potion['potion']}")
        labels.append(potion["potion"])
        parents.append(f"competence::{type_magie}::{competence}")
        values.append(1)

    return pd.DataFrame(
        {"id": ids, "label": labels, "parent": parents, "value": values}
    )