import dash
from dash import html
import dash_pro_components as pro


app = dash.Dash(__name__)

elements=[
    # Nodes elements
    {
        'id': 'default_input',
        'type': 'input',
        'data': {'label': 'Input Node'},
        'position': {'x': 50, 'y': 50}
    },
    {
        'id': 'custom_input',
        'type': 'customInput',
        'data': {
            'label': 'Custom Input',
            'style': {'background-color': '#0041d0', 'color': 'white'},
            'handleNumber': 2,
            'sourceHandleIds': ['a', 'b']
        },
        'position': {'x': 250, 'y': 50}
    },
    {
        'id': 'custom_node',
        'type': 'customDefault',
        'data': {
            'label': 'Custom Node',
            'style': {'background-color': 'black', 'color': 'white'},
            'sourceHandleNumber': 2,
            'sourceHandleIds': ['a', 'b']
        }, 
        'position': {'x': 150, 'y': 150},
        'targetPosition': 'top',
        'sourcePosition': 'bottom'
    },
    {
        'id': 'default_node',
        'data': {'label': 'Default Node'}, 
        'position': {'x': 375, 'y': 250},
        'style': {'background-color': '#b1b1b7'},
        'targetPosition': 'left',  # 'top'
        'sourcePosition': 'bottom'  # 'right'
    },
    {
        'id': 'custom_output',
        'type': 'customOutput',
        'data': {
            'label': 'Custom Output',
            'style': {'background-color': '#ff0072', 'color': 'white'},
            'handleNumber': 2,
            'targetHandleIds': ['a', 'b']
        },
        'position': {'x': 200, 'y': 350}
    },
    {
        'id': 'default_output',
        'type': 'output',
        'data': {'label': 'Default Output'},
        'position': {'x': 450, 'y': 150},
        'targetPosition': 'left'
    },

    # Edge elements
    {
        'id': 'default_input-custom_node',
        'source': 'default_input',
        'target': 'custom_node'
    },
    {
        'id': 'custom_input-custom_node',
        'source': 'custom_input',
        'target': 'custom_node',
        'sourceHandle': 'a-source-custom_input'
    },
    {
        'id': 'custom_input-default_output',
        'source': 'custom_input',
        'target': 'default_output',
        'sourceHandle': 'b-source-custom_input'
    },
    {
        'id': 'custom_node-default_node',
        'source': 'custom_node',
        'target': 'default_node',
        'sourceHandle': 'b-source-custom_node'
    },
    {
        'id': 'default_node-custom_output',
        'source': 'default_node',
        'target': 'custom_output',
        'targetHandle': 'b-target-custom_output'
    },
    {
        'id': 'custom_node-custom_output',
        'source': 'custom_node',
        'target': 'custom_output',
        'sourceHandle': 'a-source-custom_node',
        'targetHandle': 'a-target-custom_output'
    }
]

app.layout = html.Div([
    pro.FlowChart(
        id='flowchart-nodes',
        style={'width': '100%', 'height': '600px'},
        elements=elements
    )
])

if __name__ == '__main__':
    app.run_server()