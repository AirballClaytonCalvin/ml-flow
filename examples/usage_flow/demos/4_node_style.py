import dash
from dash import html, Input, Output, State
import dash_daq as daq
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
    # Edges
    {"id": "e1-2", "source": "flownode-1", "target": "flownode-2"},
    {"id": "e2-3", "source": "flownode-2", "target": "flownode-3"},
]


app.layout = html.Div([
    daq.ColorPicker(
        id='color-picker-node',
        label='Node Background Color',
        value=None
    ),
    pro.FlowChart(
        id='flowchart-nodes-style',
        elements=elements,
    )
])


@app.callback(
    Output('flowchart-nodes-style', 'elements'),
    [
        Input('color-picker-node', 'value'),
    ],
    [
        State('flowchart-nodes-style', 'selectData'),
        State('flowchart-nodes-style', 'elements')
    ]
)
def update_flowchart_style(color, node, elements):
    ctx = dash.callback_context
    if not ctx.triggered or not elements or not node:
        return dash.no_update

    for e in elements:
        if e['id'] == node[0]['id']:
            rgba_color = 'rgba({}, {}, {}, {})'.format(color['rgb']['r'], color['rgb']['g'], color['rgb']['b'], color['rgb']['a'])
            e['style'] = {
                'background': rgba_color
            }

    return elements


if __name__ == '__main__':
    app.run_server(debug=True)
