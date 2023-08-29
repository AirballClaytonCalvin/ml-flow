import dash
from dash import html
import dash_pro_components as pro

app = dash.Dash(__name__)

elements = [
    # Nodes
    {
        "id": "1",
        "type": "input", 
        "data": {"label": "Input Node"},
        "position": {"x": 250, "y": 25},
    },
    {
        "id": "2", 
        "data": {"label": "Default Node"}, 
        "position": {"x": 100, "y": 125}
    },
    {
        "id": "3",
        "type": "output",
        "data": {"label": "Output Node"},
        "position": {"x": 250, "y": 250},
    },
    # Edges
    {"id": "e1-2", "source": "1", "target": "2"},
    {"id": "e2-3", "source": "2", "target": "3"},
]


app.layout = html.Div([
    pro.FlowChart(
        elements=elements,
        children=[
            pro.FlowBackground(
                id='flow-background',
                variant="dots",  # or "lines"
                gap=16,
                size=0.6,
                color="#2a2d34",
                style={},
                className="flowBackground",
            ),
        ]
    )
])


if __name__ == '__main__':
    app.run_server()