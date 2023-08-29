import dash
from dash import html
import dash_pro_components as pro


app = dash.Dash(__name__)

elements=[
    # Nodes elements
    {
        'id': '1',
        'type': 'input', # Define node as input
        'data': {'label': 'Input Node'},
        'position': {'x': 250, 'y': 25},
    },
    {
        'id': '2', 
        'data': {'label': 'Default Node'}, 
        'position': {'x': 100, 'y': 125}
        # the absence of the type key indicates a 'default' node
    },
    {
        'id': '3',
        'type': 'output', # Define node as output
        'data': {'label': 'Output Node'},
        'position': {'x': 250, 'y': 200},
    },

    # Edge elements
    {
        'id': 'e1-2',
        'source': '1',
        'target': '2'
    },
    {
        'id': 'e2-3',
        'source': '2',
        'target': '3'
    },
]

app.layout = html.Div([
    pro.FlowChart(
        id='flowchart-elements',
        style={'width': '100%', 'height': '400px'},
        elements=elements
    )
])

if __name__ == '__main__':
    app.run_server()