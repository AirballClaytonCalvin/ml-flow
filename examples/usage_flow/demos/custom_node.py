import dash
from dash import html
import dash_pro_components as pro


app = dash.Dash(__name__)

elements_custom = [
    {
        "id": "custom-input-node",
        "type": "customInput",  # Custom input node
        "data": {
            "label": "Custom Input Node", # Define Node Label
            "style": {"borderColor": "blue"}, # Define a customizable style (optional)
            'handleNumber': 2, # define number of handles to two (optional)
            'sourceHandleIds': ['input-handle-1', 'input-handle-2'] # define handle ids (optional)
        },
        'sourcePosition': 'bottom', # define handle position to bottom (optional)
        "position": {"x": 250, "y": 25}, 
    },
    {
        "id": "custom-default-node-1", 
        "type": "customDefault",  # Custom default node
        "data": {
            "label": "Custom Default Node", # Define Node Label
            "style": {"borderColor": "green"}, # Define a customizable style (optional)
            'targetHandleNumber': 1, # define number of target handles to two (optional)
            'targetHandleIds': ['default-target-handle-1'], # define handle ids (optional)
            'sourceHandleNumber': 1, # define number of source handles to two (optional)
            'sourceHandleIds': ['default-source-handle-1', 'default-source-handle-2'] # define handle ids (optional)
        },
        'sourcePosition': 'bottom', # define source handle position to bottom (optional)
        'targetPosition': 'top', # define target handle position to top (optional)
        "position": {"x": 100, "y": 125}
    },
    {
        "id": "custom-default-node-2", 
        "type": "customDefault",
        "data": {
            "label": "Custom Default Node", 
        },
        "position": {"x": 280, "y": 125}
    },
    {
        "id": "custom-output-node", 
        "type": "customOutput",  # Custom output node
        "data": {
            "label": "Custom Output Node", # Define Node Label
            'handleNumber': 2, # define number of target handles to two (optional)
            'targetHandleIds': ['output-target-handle-1', 'output-target-handle-2'], # define handle ids (optional)
        },
        'targetPosition': 'top', # define handle position to top (optional)
        "position": {"x": 220, "y": 250}
    },
]

app.layout = html.Div([
    html.Div([
        pro.FlowChart(
            id='custom-nodes-flowchart',
            elements=elements_custom
        ),
    ]),
])


if __name__ == '__main__':
    app.run_server()