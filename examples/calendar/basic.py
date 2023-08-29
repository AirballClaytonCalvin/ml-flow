import dash
import dash_design_kit as ddk
import dash_pro_components as pro
import datetime as dt
import os
import pandas as pd


cur_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(cur_dir, "data", "calendar_data.json")
df = pd.read_json(data_path)
df.start = pd.to_datetime(df.start)
df.end = pd.to_datetime(df.end)

app = dash.Dash(__name__)
server = app.server  # expose server variable for Procfile

app.layout = ddk.App(
    show_editor=True,
    children=[
        ddk.Header(ddk.Title("Calendar Demo")),
        ddk.Card(
            width=50,
            children=[
                ddk.CardHeader(title="My Personal Calendar"),
                pro.Calendar(
                    id="personal-calendar",
                    events=df.to_dict("records"),
                    style={"height": 500, 'padding': '5px'},
                    startAccessor="start",  # pandas column
                    endAccessor="end",  # pandas column
                    defaultDate=dt.datetime(2020, 4, 22),
                    min=dt.time(hour=8, minute=30),
                    max=dt.time(hour=22),
                    popup=True,
                    selectable=True
                ),
            ]
        )
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)