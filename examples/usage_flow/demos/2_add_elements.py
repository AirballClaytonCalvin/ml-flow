import dash
from dash import html, dcc
import dash_pro_components as pro
from dash.dependencies import Input, Output, State
from random import randrange


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Label('Select Element Type'),
    dcc.Dropdown(
        id='type-dropdown',
        clearable=False,
        value='input',
        options=[
            {"label": 'Input', 'value': 'input'},
            {"label": 'Output', 'value': 'output'},
            {"label": 'Default', 'value': 'default'},
            {"label": 'Custom Input', 'value': 'customInput'},
            {"label": 'Custom Output', 'value': 'customOutput'},
            {"label": 'Custom Default', 'value': 'customDefault'},
        ]
    ),
    dcc.Input(placeholder='Insert element label', id='element-label'),
    html.Button('Add Element', id='add-element'),
    html.Button('Remove Element', id='remove-element'),
    pro.FlowChart(
        id='flowchart-add-remove',
        elements=[]
    )
])


# Callback to add or remove elements
@app.callback(
    Output('flowchart-add-remove', 'elements'),
    [
        Input('add-element', 'n_clicks'),
        Input('remove-element', 'n_clicks'),
    ],
    [
        State('type-dropdown', 'value'),
        State('element-label', 'value'),
        State('flowchart-add-remove', 'elements'),
        State('flowchart-add-remove', 'selectData')
    ]
)
def add_element(add, remove, type_value, label, elements, selected_data):

    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    trigger_source = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_source == 'add-element' and label is not None:
        new_element = {
            "id": str(add),
            "type": type_value,
            "data": {"label": label},
            "position": {"x": randrange(70, 350, 60), 'y': randrange(0, 300, 40)}
        }

        elements.append(new_element)

        return elements

    if trigger_source == 'remove-element' and selected_data is not None:
        elements = [e for e in elements if e['id'] != selected_data[0]['id']]

        return elements

    return dash.no_update
   

if __name__ == '__main__':
    app.run_server(debug=True)