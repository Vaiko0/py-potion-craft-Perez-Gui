# pages/network.py
import math

import plotly.graph_objects as go
import streamlit as st

from src.network_data import build_anomaly_report, build_graph, load_network_data


def star_layout(graph, ring_radius=5):
    inventors = sorted(
        (n for n, d in graph.nodes(data=True) if d["kind"] == "inventor"),
        key=lambda n: (graph.nodes[n]["lineage"], n),
    )
    pos = {}

    for i, inventor in enumerate(inventors):
        angle = 2 * math.pi * i / len(inventors)
        cx, cy = ring_radius * math.cos(angle), ring_radius * math.sin(angle)
        pos[inventor] = (cx, cy)

        potions = sorted(graph.neighbors(inventor))
        radius = 0.8 + 0.09 * len(potions)
        for j, potion in enumerate(potions):
            a = angle + 2 * math.pi * j / len(potions)
            pos[potion] = (cx + radius * math.cos(a), cy + radius * math.sin(a))

    orphans = sorted(
        n for n, d in graph.nodes(data=True)
        if d["kind"] == "potion" and graph.degree(n) == 0
    )
    for j, potion in enumerate(orphans):
        a = 2 * math.pi * j / max(len(orphans), 1)
        pos[potion] = (1.6 * math.cos(a), 1.6 * math.sin(a))

    return pos


st.title("Réseau des inventeurs et leur potions")

potions, inventors = load_network_data()
graph = build_graph(potions, inventors)
pos = star_layout(graph)

edge_x, edge_y = [], []
for a, b in graph.edges():
    edge_x += [pos[a][0], pos[b][0], None]
    edge_y += [pos[a][1], pos[b][1], None]

fig = go.Figure(
    go.Scatter(x=edge_x, y=edge_y, mode="lines",
               line=dict(width=0.5, color="#666"), hoverinfo="none", showlegend=False)
)

potion_nodes = [n for n, d in graph.nodes(data=True) if d["kind"] == "potion"]
fig.add_trace(go.Scatter(
    x=[pos[n][0] for n in potion_nodes], y=[pos[n][1] for n in potion_nodes],
    mode="markers",
    marker=dict(size=8, color=graph.nodes[potion_nodes[0]]["color"]),
    text=[f"{n}<br>Inventor: {graph.nodes[n]['inventor']}" for n in potion_nodes],
    hoverinfo="text", name="Potion",
))

for lineage, color in graph.graph["lineage_colors"].items():
    nodes = [n for n, d in graph.nodes(data=True)
             if d["kind"] == "inventor" and d["lineage"] == lineage]
    fig.add_trace(go.Scatter(
        x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes],
        mode="markers+text",
        marker=dict(size=[graph.nodes[n]["size"] for n in nodes], color=color,
                    line=dict(width=1, color="#0E1117")),
        text=nodes, textposition="bottom center", textfont=dict(size=10),
        hovertext=[f"{n}<br>{graph.nodes[n]['potions']} potion(s)" for n in nodes],
        hoverinfo="text", name=f"Lineage {lineage}",
    ))

fig.add_annotation(
    x=0, y=0, text="No known<br>inventor", showarrow=False,
    font=dict(size=10, color="#888"),
)

fig.update_layout(
    height=850, margin=dict(t=0, l=0, r=0, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
)
st.plotly_chart(fig, use_container_width=True)


with st.expander("Erreurs"):
    st.dataframe(build_anomaly_report(potions, inventors), hide_index=True)