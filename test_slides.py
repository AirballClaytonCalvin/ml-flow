import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State, no_update, MATCH
import dash
from utils.slides_component import SlidesComponent


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions=True

slide1 = html.Div(
    [   
        dbc.Label("slide clicked", id='label-slide-1'),
        html.Br(),
        dbc.Button(
            "Button 1",
            id="btn1",
            color="success",
            className="mr-4",
            n_clicks=0,
        )
    ]
)

slide2 = html.Div(
    [   
        dbc.Label("slide clicked", id='label-slide-2'),
        html.Br(),
        dbc.Button(
            "Button 2",
            id="btn2",
            color="success",
            className="mr-4",
            n_clicks=0,
        )
    ]
)

slide3 = html.Div(
    [   
        html.Img(src=app.get_asset_url("test_image.png"))
    ]
)

slides_list = [slide1, slide2, slide3]



slides_component = SlidesComponent(
    parent_app=app,
    slides=slides_list,
    # id='my-slides',
    # trigger_first_slide_id="trigger-first-slide",
    # trigger_previous_slide_id="trigger-previous-slide",
    # trigger_next_slide_id="trigger-next-slide",
    # trigger_last_slide_id="trigger-last-slide"
)

modal = dbc.Modal(
    [
        slides_component
    ],
    id="modal-slides",
    size="xl",
    is_open=False,
    scrollable=True
)
modal_button = html.Button(
    "Open slides",
    style={
        "width": "6rem",
        "min-width": "6rem",
        "border-radius": "1rem",
        "font-weight": "bold",
        "margin-right": "20px",
    },
    id="button-slides",
)

app.layout = dbc.Container([
    modal_button,
    modal
])


@app.callback(
    Output("modal-slides", "is_open"),
    Input("button-slides", "n_clicks"),
    State("modal-slides", "is_open"),
)
def toggle(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    Output("label-slide-1", "children"),
    Input("btn1", "n_clicks")
)
def toggle(n):
    if n:
        return f"slide clicked {n} times"
    return no_update


@app.callback(
    Output("label-slide-2", "children"),
    Input("btn2", "n_clicks")
)
def toggle(n):
    if n:
        return f"slide clicked {n} times"
    return no_update


if __name__ == "__main__":
    app.run_server(debug=True)
