import pandas as pd

def load_skills(workbook_path = "data/potions-craft.xlsx"):
    return pd.read_excel(workbook_path, sheet_name="liste-types-de-magie")
