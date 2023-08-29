import dash
from dash import html
import dash_pro_components as pro


app = dash.Dash(__name__)

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
        "data": {"label": "Default Node"}, 
        "position": {"x": 100, "y": 125}
    },
    {
        "id": "3",
        "type": "output",  # output node
        "data": {"label": "Output Node"},
        "position": {"x": 250, "y": 250},
    },
    {
        "id": 'custom-node',
        "type": 'customNode',
        "data": html.Label('test'),
        "style": {"border": '1px solid #777', "padding": 10},
        "position": {"x": 300, "y": 50},
    },
    # animated edge
    {"id": "e1-2", "source": "1", "target": "2", "animated": True},
    {"id": "e2-3", "source": "2", "target": "3"},
]


app.layout = html.Div([
    pro.FlowChart(
        elements=elements,
        children=[
            pro.FlowMiniMap()
        ]
    )
])

if __name__ == '__main__':
    app.run_server()