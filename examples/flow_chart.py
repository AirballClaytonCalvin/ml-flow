"""
Example usage for the Dash Pro Components flowchart.
"""
from copy import deepcopy

import dash_pro_components as pro
import dash
from dash import Input, Output, State, html


def add_edge(edge_params, elements, inplace=False):
    if inplace is False:
        elements = deepcopy(elements)

    src, tgt = edge_params["source"], edge_params["target"]
    edge_params["id"] = edge_params.get("id", f"e{src}-{tgt}")
    elements.append(edge_params)

    return elements


def remove_elements(elements_to_remove, elements):
    # TODO: Support inplace=True
    remove_id_set = {e["id"] for e in elements_to_remove}
    new_elements = [e for e in elements if e["id"] not in remove_id_set]

    return new_elements


def update_edge(old_edge, new_connection, elements, inplace=False):
    if inplace == False:
        elements = deepcopy(elements)

    for e in elements:
        if e["id"] == old_edge["id"]:
            print("success")
            e.update(new_connection)
            return elements

    return elements


elements = [
    {
        "id": "1",
        "type": "input",  # input node
        "data": {"label": "Input Node"},
        "position": {"x": 250, "y": 25},
    },
    # default node
    {
        "id": "2",
        # you can also pass a React component as a label
        "data": {"label": "Default Node"},
        "position": {"x": 100, "y": 125},
    },
    {
        "id": "3",
        "type": "output",  # output node
        "data": {"label": "Output Node"},
        "position": {"x": 250, "y": 250},
    },
    # animated edge
    {"id": "e1-2", "source": "1", "target": "2", "animated": True},
    {"id": "e2-3", "source": "2", "target": "3"},
]

app = dash.Dash(__name__)
styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

app.layout = html.Div(
    [
        pro.FlowChart(
            children=[pro.FlowBackground(), pro.FlowControls(), pro.FlowMiniMap()],
            elements=elements,
            id="flow-chart",
        ),
    ]
)


@app.callback(
    Output("flow-chart", "elements"),
    [
        Input("flow-chart", "edgeUpdateData"),
        Input("flow-chart", "connectData"),
        Input("flow-chart", "removeData"),
    ],
    [State("flow-chart", "elements")],
)
def update_flow_chart(edge_update, connected, removed, elements):
    ctx = dash.callback_context
    updated_prop = ctx.triggered[0]["prop_id"].split(".")[1]

    if updated_prop == "edgeUpdateData":
        new_els = update_edge(
            edge_update["oldEdge"], edge_update["newConnection"], elements
        )
        return new_els

    if updated_prop == "connectData":
        new_els = add_edge(connected, elements)
        return new_els

    if updated_prop == "removeData":
        new_els = remove_elements(removed, elements)
        return new_els

    return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)