import dash_pro_components as pro
import dash_bootstrap_components as dbc
import dash_design_kit as ddk
import dash
from dash import Output, Input, State, dcc, html, no_update
import pandas as pd
import datetime as dt
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# cur_dir = os.path.dirname(os.path.abspath(__file__))
# data_path = os.path.join(cur_dir, "data", "calendar_data.json")
# df = pd.read_json(data_path)
# df.start = pd.to_datetime(df.start)
# df.end = pd.to_datetime(df.end)

calendar = pro.Calendar(
    id="personal-calendar",
    # events=df.to_dict("records"),
    style={"height": 500, 'padding': '5px'},
    startAccessor="start",  # pandas column
    endAccessor="end",  # pandas column
    defaultDate=dt.datetime(2021, 11, 1),
    min=dt.time(hour=8, minute=30),
    max=dt.time(hour=22),
    popup=True,
    selectable=True
),

button_style = {
    "margin": "0.5rem",
    "minWidth": "200px", 
    "maxWidth": "200px"
}

btns = ddk.Card(
    id="add-elements-card",
    children=[
        dbc.Label("Add Pipeline to Calendar"),
        ddk.Row(
            id="row-date-calendar",
            style={"paddingTop": "10px"},
            children=[
                dbc.Label("Date/time: ", style={"width": "120px"}),
                ddk.Block(pro.DateTimePicker())
            ]
        ),
        ddk.Row(
            style={"paddingTop": "10px", "paddingLeft": "0.5rem"},
            children=[
                ddk.Block(
                    dbc.Select(
                        id="select-event-frequency-calendar",
                        options=[
                            {"label": "Single Event", "value": "Single Event"},
                            {"label": "Recurring Event", "value": "Recurring Event"},
                        ],
                        value="Single Event",
                    ),
                    style={
                        "minWidth": "180px",
                        "maxWidth": "180px",
                    },
                ),
                ddk.Block(
                    dbc.Input(id="input-number-recurrent-event-calendar", type="number", min=1, step=1, value=1, disabled=True)
                ),
                ddk.Block(dbc.Label("  days", style={"width": "40px", "paddingTop": "6px"}))
            ]
        ),
        html.Br(),
        ddk.Row(
            children=[
                html.Button(
                    children=[html.I(className="fas fa-plus"), " Add to Calendar"],
                    id="button-add-pipeline-to-calendar",
                    n_clicks=0,
                    style=button_style,
                ),
                html.Button(
                    children=[html.I(className="far fa-calendar-alt"), " See Calendar"],
                    id="button-see-calendar",
                    n_clicks=0,
                    style=button_style,
                ),
                dbc.Popover(
                    [
                        dbc.PopoverBody(children=calendar),
                    ],
                    id="popover-calendar",
                    target="button-see-calendar",
                    placement="right",
                    is_open=False,
                )
            ]
        )
    ],
),

app.layout = ddk.App(
    show_editor=True,
    children=[
        ddk.Block(width=25, children=btns),
        ddk.Block(width=75)
    ]
)


# Toggle Calendar Popover
@app.callback(
    Output("input-number-recurrent-event-calendar", "disabled"),
    Input("select-event-frequency-calendar", "value"),
    prevent_initial_call=True
)
def event_frequency_calendar(value):
    if value == "Recurring Event":
        return False
    return True


# Toggle Calendar Popover
@app.callback(
    Output("popover-calendar", "is_open"),
    Input("button-see-calendar", "n_clicks"),
    State("popover-calendar", "is_open"),
    prevent_initial_call=True
)
def toggle_calendar(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
