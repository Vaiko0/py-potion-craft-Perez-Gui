# potions_magic_type.py
import pandas as pd


def load_magic_type_data(workbook_path="data/potions-craft.xlsx"):
    """Charge les feuilles necessaires au sunburst."""
    return (
        pd.read_excel(workbook_path, sheet_name="liste-types-de-magie"),
        pd.read_excel(workbook_path, sheet_name="potions-inventeurs"),
    )


def build_sunburst_data(magic_types: pd.DataFrame, potions_inventeurs: pd.DataFrame) -> pd.DataFrame:
    """Construit ids/labels/parents/values pour le sunburst."""
    ids, labels, parents, values = [], [], [], []

    # niveau 1 : types de magie
    for type_magie in magic_types["type_de_magie"].unique():
        ids.append(f"type::{type_magie}")
        labels.append(type_magie)
        parents.append("")
        values.append(0)

    # niveau 2 : competences, splittees sur ";" et dupliquees par type
    for _, row in magic_types.iterrows():
        type_magie = row["type_de_magie"]
        competences = str(row["competences"]).split(";")
        for competence in competences:
            competence = competence.strip()
            ids.append(f"competence::{type_magie}::{competence}")
            labels.append(competence)
            parents.append(f"type::{type_magie}")
            values.append(0)

    # niveau 3 : potions, dupliquees sous chaque competence de leur propre type
    for _, potion in potions_inventeurs.iterrows():
        type_magie = potion["type-magie-potion"]
        potion_name = potion["potion"]

        row = magic_types.loc[magic_types["type_de_magie"] == type_magie]
        if row.empty:
            continue  # type de magie inconnu, potion ignoree

        competences = str(row.iloc[0]["competences"]).split(";")

        for competence in competences:
            competence = competence.strip()
            ids.append(f"potion::{type_magie}::{competence}::{potion_name}")
            labels.append(potion_name)
            parents.append(f"competence::{type_magie}::{competence}")
            values.append(1)

    return pd.DataFrame(
        {"id": ids, "label": labels, "parent": parents, "value": values}
    )