import dash
from dash import html, dcc
import dash_daq as daq
import dash_pro_components as pro
from dash.dependencies import Input, Output, State


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
        id='color-picker',
        label='Background Color',
        value=None
    ),

    html.Label('Border Radius'),
    dcc.Input(id='border-radius-input', value=0, type='number', min=0, max=50, step=1, style={'width': '100%'}),
    pro.FlowChart(
        id='flowchart-style',
        elements=elements,
        style={"height": '400px'}
    )
])


@app.callback(
    Output('flowchart-style', 'style'),
    [
        Input('color-picker', 'value'),
        Input('border-radius-input', 'value')
    ],
    [State('flowchart-style', 'style')]
)
def update_flowchart_style(color, radius, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    current_style['borderRadius'] = radius
    current_style['backgroundColor'] = color['hex']

    return current_style


if __name__ == '__main__':
    app.run_server(debug=True)
