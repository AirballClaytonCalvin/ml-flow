import dash
from dash import html
import dash_pro_components as pro
import dash_design_kit as ddk
from dash import ALL, MATCH, Input, Output, State, dcc, html


FA = "https://use.fontawesome.com/releases/v5.15.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[FA])


elements=[
    # Nodes elements
    {
        'id': '1',
        'type': 'customInput', # Define node as input
        'data': {'label': 'Input Node'},
        'position': {'x': 250, 'y': 25},
    },
    {
        'id': '2', 
        'data': {'label': 'Default Node'}, 
        'position': {'x': 100, 'y': 125},
        "type": "customDefault",
        # the absence of the type key indicates a 'default' node
    },

]

app.layout = ddk.App([
    pro.FlowChart(
        id='flowchart-elements',
        style={'width': '100%', 'height': '600px'},
        elements=elements,
        children=[
            pro.FlowBackground(),
            pro.FlowControls(),
            pro.FlowMiniMap()
        ]
    ),
    html.Div(id='test')
], show_editor=True)

@app.callback(
    Output('test', 'children'),
    [Input('flowchart-elements', 'connectData')]
)
def test(connectData):
    if not connectData:
        return dash.no_update
    
    print(connectData)

if __name__ == '__main__':
    app.run_server(debug=True)