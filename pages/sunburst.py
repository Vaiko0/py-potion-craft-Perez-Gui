import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from potions_magic_type import build_sunburst_data, load_magic_type_data


st.title("Potions par type de magie")

magic_types, potions_inventeurs = load_magic_type_data()
sunburst_data = build_sunburst_data(magic_types, potions_inventeurs)
total_potions = potions_inventeurs["potion"].nunique()

type_nodes = sunburst_data["id"].str.startswith("type::")
sunburst_data.loc[type_nodes, "label"] = ""
sunburst_data.loc[sunburst_data["parent"] == "", "parent"] = "root"
sunburst_data = pd.concat(
	[
		sunburst_data,
		pd.DataFrame(
			[
				{
					"id": "root",
					"label": f"{total_potions} potions",
					"parent": "",
					"value": 0,
				}
			]
		),
	],
	ignore_index=True,
)

magic_type_colors = {
	"Rouge": "#D94A4A",
	"Bleue": "#3B82F6",
	"Verte": "#3FA66B",
	"Blanche": "#E9E4D0",
	"Noire": "#34343D",
	"Pourpre": "#8E5BB7",
}


def color_for_node(node_id: str) -> str:
	parts = node_id.split("::")
	magic_type = parts[1] if len(parts) > 1 else ""
	return magic_type_colors.get(magic_type, "#9CA3AF")


node_colors = sunburst_data["id"].map(color_for_node).tolist()

figure = go.Figure(
	go.Sunburst(
		ids=sunburst_data["id"],
		labels=sunburst_data["label"],
		parents=sunburst_data["parent"],
		values=sunburst_data["value"],
		branchvalues="remainder",
		marker={"colors": node_colors},
		hovertemplate="%{label}<extra></extra>",
	)
)
figure.update_layout(margin={"t": 20, "l": 0, "r": 0, "b": 0})

st.plotly_chart(figure, use_container_width=True)
