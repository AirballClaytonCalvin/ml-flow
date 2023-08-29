import dash
from dash import html, dcc
import dash_pro_components as pro
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
    # Edges
    {"id": "e1-2", "source": "flownode-1", "target": "flownode-2"},
    {"id": "e2-3", "source": "flownode-2", "target": "flownode-3"},
]


app.layout = html.Div([
    html.Label('Select background variant'),
    dcc.Dropdown(
        id='variant-dropdown',
        clearable=False,
        value='dots',
        options=[
            {"label": 'Dots', 'value': 'dots'},
            {"label": "Lines", 'value': 'lines'}
        ]
    ),
    pro.FlowChart(
        id='flowchart-and-background',
        elements=elements,
        children=[
            pro.FlowBackground(
                id='flow-background',
                variant="dots",  # or "lines"
                gap=16,
                size=1,
                color="red",
                className="flowBackground",
            ),
        ]
    )
])


@app.callback(
    Output('flow-background', 'variant'),
    [Input('variant-dropdown', 'value')]
)
def update_flowbackground_variant(value):
    if not value:
        return dash.no_update
    return value


if __name__ == '__main__':
    app.run_server(debug=True)