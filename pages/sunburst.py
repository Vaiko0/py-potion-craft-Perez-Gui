# sunburst.py
import plotly.graph_objects as go
import streamlit as st

from potions_magic_type import build_sunburst_data, load_magic_type_data

MAGIC_COLORS = {
    "Blanche": "#F5F5F5",
    "Bleue": "#4A9EFF",
    "Verte": "#3DDC84",
    "Pourpre": "#B366E0",
    "Rouge": "#FF5C5C",
    "Noire": "#8A8F98",
}


def build_sunburst_figure(sunburst_data) -> go.Figure:
    colors = []
    texts = []
    for node_id, label in zip(sunburst_data["id"], sunburst_data["label"]):
        parts = node_id.split("::")
        colors.append(MAGIC_COLORS.get(parts[1], "#888888"))
        texts.append("" if parts[0] == "potion" else label)

    figure = go.Figure(
        go.Sunburst(
            ids=sunburst_data["id"],
            labels=sunburst_data["label"],
            parents=sunburst_data["parent"],
            values=sunburst_data["value"],
            marker=dict(colors=colors)
        )
    )
    return figure


st.title("Potions Distribution by Magic Type")

magic_types, potions_inventeurs = load_magic_type_data()
sunburst_data = build_sunburst_data(magic_types, potions_inventeurs)

figure = build_sunburst_figure(sunburst_data)
figure.update_layout(margin=dict(t=0, l=0, r=0, b=0))

st.plotly_chart(figure, use_container_width=True)
