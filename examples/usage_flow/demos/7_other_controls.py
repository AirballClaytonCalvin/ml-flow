import dash
from dash import html, dcc, Input, Output
import dash_pro_components as pro

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

]


app.layout = html.Div([
    dcc.Checklist(
        id='connectable-checklist',
        value=[],
        options=[
            {'label': 'Nodes Draggable', 'value': 'nodesDraggable'},
            {'label': 'Nodes Connectable', 'value': 'nodesConnectable'},
            {'label': 'Elements Selectable', 'value': 'elementsSelectable'},
            {'label': 'Zoom on Scrool', 'value': 'zoomOnScroll'},
            {'label': 'Pan on Scrool', 'value': 'panOnScroll'},
            {'label': 'Pane Moveable', 'value': 'paneMoveable'},
        ],
    ),
    pro.FlowChart(
        id='flowchart-interaction',
        elements=elements, 
        nodesDraggable=False,
        nodesConnectable=False,
        elementsSelectable=False,
        zoomOnScroll=False,
        panOnScroll=False,
        paneMoveable=False  
    )
])

@app.callback(
    [
        Output('flowchart-interaction', 'nodesDraggable'),
        Output('flowchart-interaction', 'nodesConnectable'),
        Output('flowchart-interaction', 'elementsSelectable'),
        Output('flowchart-interaction', 'zoomOnScroll'),
        Output('flowchart-interaction', 'panOnScroll'),
        Output('flowchart-interaction', 'paneMoveable')
    ],
    [Input('connectable-checklist', 'value')]
)
def update_connectable(values):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    outputs = [
        'nodesDraggable', 
        'nodesConnectable', 
        'elementsSelectable', 
        'zoomOnScroll',
        'panOnScroll',
        'paneMoveable'
    ]
    output = [True if e in values else False for e in outputs]

    return output


if __name__ == '__main__':
    app.run_server(debug=True)