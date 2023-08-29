import dash
from dash import html
import dash_pro_components as pro
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

elements = [
    # Nodes
    {
        "id": "flownode-1",
        "type": "input",
        "data": {"label": "Input Node"},
        "position": {"x": 250, "y": 25},
    },
    {
        "id": "flownode-2",
        "data": {"label": "Default Node"}, 
        "position": {"x": 100, "y": 125}
    },
    {
        "id": "flownode-3",
        "type": "output",
        "data": {"label": "Output Node"},
        "position": {"x": 250, "y": 250},
    },
    # Edge elements
    {
        "id": "e1-2",
        "source": "flownode-1",
        "target": "flownode-2"
    },
    {
        "id": "e2-3",
        "source": "flownode-2",
        "target": "flownode-3"
    }
]

app.layout = html.Div([
    pro.FlowChart(
        id="flowchart-interaction",
        elements=elements
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("More information about selected node"),
            dbc.ModalBody(id="modal-flowchart-content"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-flowchart", className="ml-auto")
            ),
        ],
        id="modal-flowchart",
    ),
])

@app.callback(
    [
        Output("modal-flowchart", "is_open"),
        Output("modal-flowchart-content", "children")
    ],
    [
        Input("close-flowchart", "n_clicks"),
        Input("flowchart-interaction", "selectData")
    ]
)

def open_modal(n_clicks, data):
    ctx = dash.callback_context
    if "close" in ctx.triggered[0]["prop_id"]:
        return False, dash.no_update

    if data:
        return True, "You selected " + ", ".join(
            [
                "a {} node".format(s["type"]) for s in data
            ]
        )

    return dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)