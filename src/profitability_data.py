from pathlib import Path
import pandas as pd
from src.convert_units import convert_to_pincee

_anomalies: list[dict[str, str]] = []


def get_anomalies() -> pd.DataFrame:
    return pd.DataFrame(_anomalies)


def _log_anomaly(potion: str, type_: str, valeur: str, action: str):
    _anomalies.append({"potion": potion, "type": type_, "valeur": valeur, "action": action})


def calculate_ingredient_cost(ingredient: str, quantity: float, unit: str, ingredients: pd.DataFrame):
    ingredient_rows = ingredients[ingredients["ingredients"] == ingredient]
    if ingredient_rows.empty:
        return None

    ingredient_data = ingredient_rows.iloc[0]
    quantity_in_pincee = convert_to_pincee(float(quantity), str(unit))
    weight_in_pincee = float(ingredient_data["poids_pincee"])
    price = float(ingredient_data["prix"])

    return quantity_in_pincee / weight_in_pincee * price


def calculate_potion_profit(potion: pd.Series, ingredients: pd.DataFrame, diluants: pd.DataFrame,):
    potion_name = str(potion["potion"])
    ingredient_cost = 0.0

    for number in range(1, 5):
        ingredient_name = potion.get(f"ingredient_{number}")
        quantity = potion.get(f"quantite_{number}")
        unit = potion.get(f"unite_{number}")

        if pd.isna(ingredient_name) or pd.isna(quantity) or pd.isna(unit):
            continue

        cost = calculate_ingredient_cost(
            str(ingredient_name), float(quantity), str(unit), ingredients
        )
        if cost is None:
            _log_anomaly(
                potion=potion_name,
                type_="ingredient_inconnu",
                valeur=str(ingredient_name),
                action="potion exclue du calcul de rentabilite",
            )
            return None

        ingredient_cost += cost

    diluant_name = potion.get("diluant")
    diluant_cost = 0.0
    if not pd.isna(diluant_name):
        diluant_rows = diluants[diluants["diluant"] == diluant_name]
        diluant_cost = float(diluant_rows.iloc[0]["prix"])

    selling_price = float(potion["prix"])
    total_cost = ingredient_cost + diluant_cost

    return {
        "potion": potion_name,
        "prix_vente": selling_price,
        "cout_ingredients": ingredient_cost,
        "cout_diluant": diluant_cost,
        "cout_total": total_cost,
        "benefice": selling_price - total_cost,
    }


def calculate_profitability(potions: pd.DataFrame, ingredients: pd.DataFrame, diluants: pd.DataFrame,):
    results = [
        calculate_potion_profit(potion, ingredients, diluants)
        for _, potion in potions.iterrows()
    ]
    results = [r for r in results if r is not None]
    return pd.DataFrame(results).sort_values("benefice", ascending=False).reset_index(drop=True)


def top_10_profitable_potions(potions: pd.DataFrame, ingredients: pd.DataFrame, diluants: pd.DataFrame,):
    return calculate_profitability(potions, ingredients, diluants).head(10)



def load_profitability_data(workbook_path = "data/potions-craft.xlsx",):
    workbook_path = Path(workbook_path)
    return (pd.read_excel(workbook_path, sheet_name="potions"), pd.read_excel(workbook_path, sheet_name="liste-ingredients"),
        pd.read_excel(workbook_path, sheet_name="prix-diluants"))

