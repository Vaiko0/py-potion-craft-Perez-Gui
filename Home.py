import streamlit as st

from src.network_data import build_anomaly_report, load_network_data
from src.profitability_data import (
    get_anomalies,
    load_profitability_data,
    top_10_profitable_potions,
)

st.set_page_config(
    page_title="Potion Craft",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Potion Craft")
st.caption("Dashboard Département des archives magiques")

potions, ingredients, diluants = load_profitability_data()
top_potions = top_10_profitable_potions(potions, ingredients, diluants)
excluded = get_anomalies()

_, inventors = load_network_data()
potions_inventeurs, _ = load_network_data()
missing_inventor = potions_inventeurs["inventeur"].isna().sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Potions", potions["potion"].nunique())
col2.metric("Ingrédients", len(ingredients))
col3.metric("Inventeurs", len(inventors))
col4.metric(
    "Anomalies",
    (excluded["potion"].nunique() if not excluded.empty else 0) + int(missing_inventor),
    help="Potions excluded from profitability (unknown ingredient) "
    "+ potions with no known inventor.",
)

st.divider()

best = top_potions.iloc[0]
st.subheader("Potions la plus rentable")
st.metric(best["potion"], f"{best['benefice']:.2f} gold")

st.divider()

st.subheader("Explorer")
left, right = st.columns(2)

with left:
    st.page_link("pages/profitability.py", label="Profitability: top 10 potions", icon="💰")
    st.page_link("pages/sunburst.py", label="Sunburst: magic types, skills, potions", icon="🌞")

with right:
    st.page_link("pages/radarchart.py", label="Radar: potions per skill", icon="🕸️")
    st.page_link("pages/network.py", label="Network: inventors and their potions", icon="🔗")