import dash_bootstrap_components as dbc
from dash import dcc, html


slide1 = html.Div(
    dcc.Markdown(
    """
    ### Motivation for a ML Pipeline GUI app 

    MLOps life cycle management is a daunting challenge for many businesses:
    - requires integration of a wide range of tech experts, from data handling to governance 
    - difficult to represent its complexity in an overarching, higher abstract level
    - it usually alienates non-tech company's professionals

    A ML Pipeline GUI could be a good starting point to tackle those issues:
    - visual representations goes where code and configuration files cannot go
    - interactivity opens up endless possibilities of inspection at different stages
    - highly customizable pipelines makes it more intuitive to modify and test different MLOps designs
    - provides encompassing integration of the MLOps lifecycle stages, from data handling to governance

    """
    )
)

slide2 = html.Div(
    dcc.Markdown(
    """
    ### ML Pipeline GUI - nuts and bolts

    - **Dash Pro Components** - FlowChart, Tour, Ag-Grid, DateTimePicker, Calendar and CodeTextArea
    - **Dash Design Kit**     - polished style and theme editor
    - **Dash 2.0**            - long callbacks and All-in-one components
    - **Dash Enterprise**     - easy deployment and app management
    
    All these resources and functionalities are available in Dash Enterprise 5

    """
    )
)

slides_list = [slide1, slide2]
