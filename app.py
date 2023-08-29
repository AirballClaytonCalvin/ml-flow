import dash
import dash_bootstrap_components as dbc
import dash_design_kit as ddk
import dash_pro_components as pro
from dash import ALL, MATCH, Input, Output, State, dcc, html, no_update
from dash.long_callback import CeleryLongCallbackManager
from sklearn import datasets
from dash_extensions import Download
from celery import Celery
import redis
from redis import DataError
import json
import time
from datetime import datetime, timedelta
import datetime as dt
import uuid
import base64

from config import (
    REDIS_CELERY_BACKEND_URL,
    REDIS_CELERY_BROKER_URL,
    REDIS_DATA_URL,
    REDIS_EXPIRY,
    SHOW_DDK_EDITOR,
)
from utils.themes import preset_themes
from utils.pipeline_example import create_pipeline_example
from utils.tour import tour, tour_test
from utils.utils import (
    handle_add_dataset,
    handle_add_model,
    handle_add_operation,
    handle_add_preprocessing,
    handle_add_service,
    handle_connect_data,
    update_elements_from_popovers,
    create_dag,
    process_pipeline_step,
    update_node_layout,
    create_dataset_popover_body,
    create_preprocessing_popover_body,
    create_model_popover_body,
    create_operation_popover_body,
    create_service_popover_body,
    dag_to_elements
)
from utils.about_slides import slides_list
from utils.slides_component import SlidesComponent


# TODO - Bootstrap Themes are important to fix some styles (e.g. Slides), but it's still breaking other styles
# This should be fixed in the DDK/Bootstrap interface changes: https://github.com/plotly/dash-design-kit/pull/1145
external_stylesheets = [
    "https://use.fontawesome.com/releases/v5.15.2/css/all.css",  # FontAwesome
]

app = dash.Dash(
    __name__,
    title="ML Pipeline GUI",
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
server = app.server  # expose server variable for Procfile

# Celery and Redis
celery_app = Celery(
    __name__,
    broker=REDIS_CELERY_BROKER_URL,
    backend=REDIS_CELERY_BACKEND_URL,
    result_expires=REDIS_EXPIRY
)
long_callback_manager = CeleryLongCallbackManager(celery_app)

redis_instance = redis.StrictRedis.from_url(REDIS_DATA_URL)

# Modal About
slides_component = SlidesComponent(
    parent_app=app,
    id='myslides',
    slides=slides_list,
)

modal_about = dbc.Modal(
    children=[slides_component],
    id="modal-about",
    size="xl",
    is_open=False,
    scrollable=False
)

# Page header
page_header = ddk.Header(
    id="app-page-header",
    style={"justify-content": "space-between"},
    children=[
        ddk.Logo(app.get_asset_url("logo.svg")),
        ddk.Title("ML Pipeline GUI"),
        ddk.Menu([
            html.Button(
                "Tour",
                style={
                    "width": "6rem",
                    "min-width": "6rem",
                    "border-radius": "1rem",
                    "font-weight": "bold",
                    "margin-right": "20px",
                },
                id="tour-btn",
            ),
            html.Button(
                "About",
                style={
                    "width": "6rem",
                    "min-width": "6rem",
                    "border-radius": "1rem",
                    "font-weight": "bold",
                    "margin-right": "20px",
                },
                id="button-about",
            ),
        ]),
        tour,
        tour_test,
        modal_about
    ],
)

# Pipeline Controls pannel
calendar = pro.Calendar(
    id="events-calendar",
    style={"height": 500, 'padding': '5px'},
    startAccessor="start",  # pandas column
    endAccessor="end",  # pandas column
    defaultDate=dt.datetime(2021, 11, 1),
    popup=True,
    selectable=True
)

button_style = {
    "padding": ".5rem",
    "margin": "0.5rem",
    "borderRadius": "1rem",
    "fontWeight": "bold",
}

button_style_2 = {
    "borderRadius": "1rem",
    "padding": ".5rem",
    "margin": "0.5rem",
    "minWidth": "200px", 
    "maxWidth": "200px"
}

button_style_3 = {
    "margin": "0.5rem",
    "minWidth": "200px", 
    "maxWidth": "200px"
}

card_calendar = ddk.Card(
    children=[
        ddk.CardHeader(title="Add Pipeline to Calendar"),
        ddk.Block(
            children=[
                dbc.Row(
                    style={"padding-top": "1rem"},
                    children=[
                        dbc.Col(
                            dbc.Label("Name: "),
                            md=4,
                            lg=4,
                            xl=4
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="input-name-event-calendar",
                                type="text",
                                style={"display": "block", "width": "100%"}
                            ),
                            md=8,
                            lg=8,
                            xl=8
                        )
                    ]
                ),
                dbc.Row(
                    id="row-date-calendar",
                    style={"padding-top": "1rem"},
                    children=[
                        dbc.Col(
                            dbc.Label("Date/time: "),
                            md=4,
                            lg=4,
                            xl=4
                        ),
                        dbc.Col(
                            pro.DateTimePicker(
                                id='calendar-datetime-picker',
                                style={"display": "block", "width": "100%"}
                            ),
                            md=8,
                            lg=8,
                            xl=8
                        )
                    ]
                ),
                dbc.Row(
                    style={"padding-top": "1rem"},
                    children=[
                        dbc.Col(
                            dbc.Select(
                                id="select-event-frequency-calendar",
                                options=[
                                    {"label": "Single Event", "value": "Single Event"},
                                    {"label": "Recurring Event", "value": "Recurring Event"},
                                ],
                                value="Single Event",
                            ),
                            lg=6,
                            xl=6
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="input-number-recurrent-event-calendar",
                                type="number",
                                min=1,
                                step=1,
                                value=1,
                                disabled=True
                            ),
                            lg=4,
                            xl=4
                        ),
                        dbc.Col(
                            dbc.Label("days"),
                            style={
                                "display": "flex",
                                "align-content": "center",
                                "justify-content": "flex-start"
                            },
                            lg=2,
                            xl=2
                        )
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            html.Button(
                                children=[html.I(className="fas fa-plus"), " Add to Calendar"],
                                id="button-add-pipeline-to-calendar",
                                n_clicks=0,
                                style={"display": "block", "width": "100%", "borderRadius": "1rem"},
                            ),
                            style={"padding-top": "1rem"},
                        ),
                        dbc.Col(
                            children=[
                                html.Button(
                                    children=[html.I(className="far fa-calendar-alt"), " See Calendar"],
                                    id="button-see-calendar",
                                    n_clicks=0,
                                    style={"display": "block", "width": "100%", "borderRadius": "1rem"},
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
                            ],
                            style={"padding-top": "1rem"},
                        )
                    ]
                )
            ]
        )
    ],
)

pipeline_controls = ddk.Block(
    width=25,
    children=[
        ddk.Card(
            id="card-add-nodes",
            children=[
                ddk.CardHeader(title='Add nodes'),
                ddk.Block(
                    children=[
                        dbc.Row(
                            style={"padding-top": "1rem", "padding-bottom": "1rem"},
                            children=[
                                dbc.Col(
                                    dbc.Label("Flow direction:"),
                                    lg=6,
                                    xl=4
                                ),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Vertical", "value": 1},
                                            {"label": "Horizontal", "value": 2},
                                        ],
                                        value=1,
                                        id="flowdirections-input",
                                        inline=True
                                    ),
                                    lg=6,
                                    xl=8
                                )
                            ],
                        ),
                        ddk.Block(
                            children=[
                                html.Button(
                                    children=[html.I(className="fas fa-plus"), " Dataset"],
                                    id="button-add-dataset",
                                    n_clicks=0,
                                    style=button_style,
                                ),
                                html.Button(
                                    children=[html.I(className="fas fa-plus"), " Preprocessing"],
                                    id="button-add-preprocessing",
                                    n_clicks=0,
                                    style=button_style,
                                ),
                                html.Button(
                                    children=[html.I(className="fas fa-plus"), " Model"],
                                    id="button-add-model",
                                    n_clicks=0,
                                    style=button_style,
                                ),
                                html.Button(
                                    children=[html.I(className="fas fa-plus"), " Operation"],
                                    id="button-add-operation",
                                    n_clicks=0,
                                    style=button_style,
                                ),
                                html.Button(
                                    children=[html.I(className="fas fa-plus"), " Service"],
                                    id="button-add-service",
                                    n_clicks=0,
                                    style=button_style,
                                ),
                            ]
                        )
                    ]
                )
            ],
        ),
        card_calendar,
        ddk.Card(
            children=[
                dbc.Row(
                    style={"padding-top": "0.10rem"},
                    children=[
                        dbc.Col(
                            html.Button(
                                [html.I(className="far fa-trash-alt"), "Clean Pipeline"],
                                id="button-clean-pipeline",
                                style={"display": "block", "width": "100%", "borderRadius": "1rem"},
                            )
                        )
                    ],
                ),
                dbc.Row(
                    style={"padding-top": "0.70rem"},
                    children=[
                        dbc.Col([
                            html.Button(
                                children=[
                                    html.I(className="fas fa-save"),
                                    "Save Pipeline",
                                ],
                                id="save-pipeline-btn",
                                style={"display": "block", "width": "100%", "borderRadius": "1rem"},
                            ),
                            Download(id='download-pipeline')
                        ])
                    ],
                ),
                dbc.Row([
                    dbc.Col([
                        dcc.Upload(
                            html.Button(
                                children=[
                                    html.I(className="fas fa-upload"),
                                    "Load Pipeline",
                                ],
                                style={"display": "block", "width": "100%", "borderRadius": "1rem"},
                            ),
                            id="load-pipeline-btn",
                        )
                    ])
                ], style={"padding-top": "0.70rem"},),
                dbc.Row(
                    style={"padding-top": "0.70rem"},
                    children=[
                        dbc.Col(
                            html.Button(
                                [html.I(className="fas fa-magic"), "Show Example"],
                                id="button-pipeline-example",
                                style={"display": "block", "width": "100%", "borderRadius": "1rem"},
                            )
                        )
                    ],
                ),
            ],
        ),
    ],
)

# Pipeline Chart
pipeline_chart = ddk.Block(
    width=75,
    children=[
        ddk.Block(
            children=[
                ddk.Card(
                    children=[
                        pro.FlowChart(
                            id="flowchart",
                            deletableNodes=False,
                            elements=[],
                            onlyRenderVisibleElements=False,
                            children=[
                                pro.FlowBackground(
                                    variant="dots",  # or "lines"
                                    gap=16,
                                    size=0.6,
                                    color="#2a2d34",
                                    style={},
                                    className="flowBackground",
                                ),
                                pro.FlowControls(
                                    showZoom=True,
                                    showFitView=True,
                                    showInteractive=True,
                                    style={},
                                    className="flowControls",
                                ),
                            ],
                        ),
                        dcc.Store(id="pipeline-dag"),
                    ],
                    id="flowchart-card",
                ),
                ddk.Card(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Button(
                                        children=[
                                            html.I(className="fas fa-play"),
                                            "  Run Pipeline",
                                        ],
                                        style={
                                            "margin-bottom": ".8rem",
                                            "border-radius": "1rem",
                                            "font-weight": "bold",
                                            "display": "block",
                                            "width": "100%",
                                        },
                                        id="run-pipeline-btn",
                                    ),
                                    md=3,
                                    lg=3,
                                    xl=2
                                ),
                                dbc.Col(
                                    html.Button(
                                        children=[
                                            html.I(className="fas fa-times"),
                                            "  Cancel Run",
                                        ],
                                        style={
                                            "margin-bottom": ".8rem",
                                            "border-radius": "1rem",
                                            "font-weight": "bold",
                                            "display": "block",
                                            "width": "100%",
                                        },
                                        id="cancel-run-btn",
                                    ),
                                    md=3,
                                    lg=3,
                                    xl=2
                                ),
                                dbc.Col(
                                    html.Button(
                                        children=[
                                            html.I(className="fas fa-chart-bar"),
                                            "  Show Results",
                                        ],
                                        style={
                                            "margin-bottom": ".8rem",
                                            "border-radius": "1rem",
                                            "font-weight": "bold",
                                            "display": "block",
                                            "width": "100%",
                                        },
                                        id="show-results-btn",
                                        disabled=True
                                    ),
                                    md=3,
                                    lg=3,
                                    xl=2
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(dbc.ModalTitle("Results")),
                                        dbc.ModalBody(id="modal-body"),
                                    ],
                                    id="results-modal",
                                    size="lg",
                                    is_open=False,
                                ),
                            ]
                        ),
                        dbc.Progress(
                            id="update-progress",
                            style={"visibility": "hidden"},
                            animated=True, 
                            striped=True
                        ),
                        dbc.Textarea(
                            id="output-textarea",
                            disabled=True,
                            style={"height": "230px"}
                        ),
                    ],
                    id="run-pipeline-card",
                ),
            ]
        )
    ]
)

# App layout
app.layout = ddk.App(
    show_editor=SHOW_DDK_EDITOR,
    #theme=preset_themes['dark'],
    children=[
        dcc.Store(id='session-id', storage_type='memory'),
        dcc.Store(id='flowdirection-store', data='vertical'),
        dcc.Store(id='flowchart-dag-running-store', data=dict(), storage_type='memory'),
        dcc.Store(id='run-pipeline-current-data', storage_type='memory'),
        dcc.Store(id='pipeline-last-proccess', storage_type='memory'),
        dbc.Button(id='trigger-long-callback', style={'display': 'none'}),
        dbc.Button(id='inner-cancel-callback', style={"display": 'none'}),
        page_header,
        dbc.Alert(
            dismissable=True,
            is_open=False,
            duration=10000,
            color="info",
            id="alert-run-pipeline",
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        ),
        dbc.Alert(
            dismissable=True,
            is_open=False,
            duration=10000,
            color="info",
            id="alert-finished-pipeline",
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        ),
        ddk.Row(
            id="overall-app-row",
            children=[
                pipeline_controls,
                pipeline_chart,
            ],
        ),
        html.Div(children=[], id="div-popovers")
    ],
)


# Generate session ID on page load
@app.callback(
    dict(session_id=Output("session-id", "data")),
    dict(session_id=Input("session-id", "data")),
)
def generate_session_id(session_id):
    if not session_id:
        return dict(session_id=str(uuid.uuid4()))
    else:
        raise dash.exceptions.PreventUpdate


# Toggle Modal
@app.callback(
    Output("results-modal", "is_open"),
    [Input("show-results-btn", "n_clicks")],
    [State("results-modal", "is_open")],
)
def toggle_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


# Calendar
@app.callback(
    Output('events-calendar', 'events'),
    Input('button-add-pipeline-to-calendar', 'n_clicks'),
    [
        State('input-name-event-calendar', 'value'),
        State('calendar-datetime-picker', 'value'),
        State('select-event-frequency-calendar', 'value'),
        State('input-number-recurrent-event-calendar', 'value'),
        State('events-calendar', 'events')
    ]
)
def add_to_calendar(n_clicks, event_name, event_datetime, event_frequency, frequency, curr_events):

    ctx = dash.callback_context
    if not ctx.triggered or event_name is None or event_datetime is None:
        return no_update

    if curr_events is None:
        curr_events = list()

    datetime_start = datetime.fromisoformat(event_datetime)
    if event_frequency == 'Single Event':
        new_event = {
            "id": len(curr_events) + 1,
            "title": event_name,
            "start": event_datetime,
            "end": (datetime_start + timedelta(minutes=30)).isoformat()
        }
        curr_events.append(new_event)

        return curr_events

    # Create recurring events for one year
    for i in range(365 // frequency):
        new_event = {
            "id": len(curr_events) + 1,
            "title": event_name,
            "start": (datetime_start + timedelta(days=frequency*i)).isoformat(),
            "end": (datetime_start + timedelta(days=frequency*i, minutes=30)).isoformat(),
        }
        curr_events.append(new_event)

    return curr_events

"""
This intermediary function is responsible for creating the DAG and saving in redis to
be used by others.
This is done because if we directly take the reference of the elements in the 
long callback with a STATE for example, tasks are passed to celerey whenever any 
element status update occurs.
"""
@app.callback(
    [
        Output('trigger-long-callback', 'n_clicks'),
        Output('alert-run-pipeline', 'children'),
        Output('alert-run-pipeline', 'color'),
        Output('alert-run-pipeline', 'is_open'),
        Output("download-pipeline", 'data')
    ],
    [
        Input('run-pipeline-btn', 'n_clicks'),
        Input('save-pipeline-btn', 'n_clicks'),
        Input('button-clean-pipeline', 'n_clicks'),
    ],
    [
        State('trigger-long-callback', 'n_clicks'),
        State('flowchart', 'elements'),
        # Get values and index from elements with params, zip it and hash by index to get the right parameters for each function
        # Preprocessing sliders
        State({"type": "popover-body-preprocessing-slider", "index": ALL}, 'value'),
        State({"type": "popover-body-preprocessing-slider", "index": ALL}, 'id'),
        # Service deploy
        State({'type': 'popover-service-deploy-checklist', 'index': ALL}, 'value'),
        State({'type': 'popover-service-deploy-checklist', 'index': ALL}, 'id'),
        # Service email
        State({'type': 'popover-service-email', 'index': ALL}, 'value'),
        State({'type': 'popover-service-email', 'index': ALL}, 'id'),
        # Session ID
        State("session-id", "data"),
    ],
    prevent_initial_call=True
)
def update_dag_handler(
    trigger_run_pipeline,
    trigger_save_pipeline,
    trigger_clean_pipeline,
    n_clicks_trigger_pipeline,
    elements,
    sliders_values,
    sliders_indexes,
    deploy_values,
    deploy_indexes,
    email_values,
    email_indexes,
    session_id
):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, dash.no_update

    trigger_source = ctx.triggered[0]["prop_id"].split(".")[0]

    if 'button-clean-pipeline' in trigger_source:
        return no_update, no_update, no_update, no_update, dash.no_update

    if not elements:
        return no_update, "No elements in pipeline!", "danger", True, dash.no_update

    # This will read from all elements inside Popovers and create the DAG
    sliders_aux = {idx['index']: val for val, idx in zip(sliders_values, sliders_indexes)}
    deploy_aux = {idx['index']: val for val, idx in zip(deploy_values, deploy_indexes)}
    email_aux = {idx['index']: val for val, idx in zip(email_values, email_indexes)}

    extra_params = {**sliders_aux, **deploy_aux, **email_aux}
    flowchart_dag = create_dag(elements, params=extra_params)

    if not flowchart_dag:
        redis_instance.hset(name=session_id, key='flowchart_dag', value=json.dumps({}))
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)
        return no_update, "Something went wrong on DAG creation", "danger", True

    redis_instance.hset(name=session_id, key='flowchart_dag', value=json.dumps(flowchart_dag))
    redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

    if trigger_source == 'save-pipeline-btn':
        # Download pipeline
        file_data = dict(
            content=json.dumps(flowchart_dag, indent=4),
            filename='dash_pipeline_dag.json'
        )
        return no_update, "DAG saved to file!", "success", True, file_data

    if trigger_source == 'run-pipeline-btn':
        if n_clicks_trigger_pipeline is None:
            n_clicks_trigger_pipeline = 0
        return n_clicks_trigger_pipeline + 1, "Pipeline started!", "primary", True, dash.no_update


# Run pipeline long callback
@app.long_callback(
    output=[
        Output("alert-finished-pipeline", "children"),
        Output("alert-finished-pipeline", "color"),
        Output("alert-finished-pipeline", "is_open"),
        Output("modal-body", "children"),
        Output("show-results-btn", "disabled")
    ],
    inputs=[Input("trigger-long-callback", "n_clicks")],
    state=[State("session-id", "data")],
    running=[
        (Output("run-pipeline-btn", "disabled"), True, False),
        (Output("cancel-run-btn", "disabled"), False, True),
        (Output('button-clean-pipeline', 'disabled'), True, False),
        (Output('button-pipeline-example', 'disabled'), True, False),
        (
            Output("update-progress", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"},
        ),
    ],
    cancel=[Input("cancel-run-btn", "n_clicks")],
    manager=long_callback_manager,
    progress=[
        Output("run-pipeline-current-data", "data"),
        Output("update-progress", "value"),
        Output("update-progress", "label")
    ],
    prevent_initial_call=True,
)
def run_pipeline_long(set_progress, n_clicks, session_id):
    flowchart_dag = json.loads(redis_instance.hget(name=session_id, key='flowchart_dag'))

    if not flowchart_dag:
        return "No DAG registered...", "danger", True, None, True

    updating_element = dict(first_run=True)
    count_size = 0
    for k, v in flowchart_dag.items():
        if isinstance(v, list):
            count_size += len(v)
        else:
            count_size += 1

    count = 100/count_size
    add_count = 100/count_size
    log_text = "Pipeline started..."
    pipeline_results = None
    for _, v in flowchart_dag.items():
        for e in v:
            updating_element['element_id'] = e['element_id']
            updating_element['status'] = 'running'
            set_progress([updating_element, int(count), f'running {e["option"]}'])
            count += add_count
            if updating_element.get('first_run', False):
                del updating_element['first_run']
            if not e.get('type', False):
                time.sleep(1)
                return f"Pipeline aborted!", "danger", True, None, True
            try:
                if e["function"] == "run_compare_and_select":
                    pipeline_results = process_pipeline_step(step=e, redis_instance=redis_instance, session_id=session_id)
                else:
                    process_pipeline_step(step=e, redis_instance=redis_instance, session_id=session_id)
                e["status"] = "done"
                redis_instance.hset(name=session_id, key='flowchart_dag', value=json.dumps(flowchart_dag))
                redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

            except (RuntimeError, TypeError, NameError, ValueError, SyntaxError, KeyError, DataError) as error:
                e["status"] = "failed"
                redis_instance.hset(name=session_id, key='flowchart_dag', value=json.dumps(flowchart_dag))
                redis_instance.expire(name=session_id, time=REDIS_EXPIRY)
                return f"Pipeline failed at {e['type']}: {e['option']}. Error: {error}", "danger", True, None, True

    return "Pipeline finished successfully!", "success", True, pipeline_results, False


@app.callback(
    [
        Output("flowchart", "elements"),
        Output("div-popovers", "children"),
        Output("output-textarea", "value"),
        Output('flowchart-dag-running-store', 'data'),
        Output('pipeline-last-proccess', 'data'),
        Output('overall-app-row', 'children')
    ],
    [
        Input('load-pipeline-btn', 'contents'),
        Input("button-add-dataset", "n_clicks"),
        Input("button-add-preprocessing", "n_clicks"),
        Input("button-add-model", "n_clicks"),
        Input("button-add-operation", "n_clicks"),
        Input("button-add-service", "n_clicks"),
        Input({"type": "div-popover-dropdown-dataset", "index": ALL}, "value"),
        Input({"type": "div-popover-dropdown-preprocessing", "index": ALL}, "value"),
        Input({"type": "div-popover-dropdown-model", "index": ALL}, "value"),
        Input({"type": "div-popover-dropdown-operation", "index": ALL}, "value"),
        Input({"type": "div-popover-dropdown-service", "index": ALL}, "value"),
        Input("button-clean-pipeline", "n_clicks"),
        Input("button-pipeline-example", "n_clicks"),
        Input("flowchart", "connectData"),
        Input('run-pipeline-current-data', 'data')
    ],
    [
        State("flowchart", "elements"),
        State("div-popovers", "children"),
        State("output-textarea", "value"),
        State('flowdirection-store', 'data'),
        State('pipeline-last-proccess', 'data'),
        State("session-id", "data")
    ],
)
def context_handler(
    upload_content,
    add_data_clicks,
    add_preprocessing_clicks,
    add_model_clicks,
    add_operation_clicks,
    add_service_clicks,
    select_dataset,
    select_preprocessing,
    select_model,
    select_operation,
    select_service,
    clean_click,
    pipeline_example,
    connect_data,
    updating_element,
    elements,
    popovers,
    textarea,
    flow_direction,
    pipeline_last_proccess,
    session_id
):

    ctx = dash.callback_context
    if not ctx.triggered:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )

    trigger_source = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_source == 'run-pipeline-current-data' and isinstance(updating_element, dict) and updating_element != pipeline_last_proccess:
        dt_string = "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "]  "

        if updating_element.get('first_run', False):
            textarea = dt_string + "Pipeline started..."

        element = [e for e in elements if e['id'] == updating_element['element_id']][0]

        cancel_pipeline, output_elements = update_node_layout(element, elements)

        if cancel_pipeline:
            text = dt_string + f"Node {element['data'].get('label', '')} not defined"
        else:
            text = dt_string + "running {}".format(element["data"]["description"])

        current_text = [textarea if textarea is not None else ""][0]
        output_text = current_text + "\n" + text

        return (
                output_elements,
                no_update,
                output_text,
                no_update,
                updating_element,
                no_update
            )

    if trigger_source == 'load-pipeline-btn':
        _, content_string = upload_content.split(',')
        bs4decode = base64.b64decode(content_string)
        json_string = bs4decode.decode('utf8').replace("'", '"')
        flowchart_dag = json.loads(json_string)

        output_elements, output_popovers = dag_to_elements(
            dag=flowchart_dag,
            redis_instance=redis_instance,
            session_id=session_id
        )

        return (
            output_elements,
            output_popovers,
            no_update,
            no_update,
            no_update,
            no_update
        )


    # Add Dataset Button
    if trigger_source == "button-add-dataset" and add_data_clicks > 0:
        elements, popovers = handle_add_dataset(
            elements=elements, popovers=popovers, id_index=add_data_clicks, flow_direction=flow_direction
        )
        return (
            elements,
            popovers,
            no_update,
            no_update,
            no_update,
            no_update
        )

    # Add Preprocessing Button
    if trigger_source == "button-add-preprocessing" and add_preprocessing_clicks > 0:
        elements, popovers = handle_add_preprocessing(
            elements=elements, popovers=popovers, id_index=add_preprocessing_clicks, flow_direction=flow_direction
        )
        return (
            elements,
            popovers,
            no_update,
            no_update,
            no_update,
            no_update
        )

    # Add Model Button
    if trigger_source == "button-add-model" and add_model_clicks > 0:
        elements, popovers = handle_add_model(
            elements=elements, popovers=popovers, id_index=add_model_clicks, flow_direction=flow_direction
        )
        return (
            elements,
            popovers,
            no_update,
            no_update,
            no_update,
            no_update
        )

    # Add Operation Button
    if trigger_source == "button-add-operation" and add_operation_clicks > 0:
        elements, popovers = handle_add_operation(
            elements=elements, popovers=popovers, id_index=add_operation_clicks, flow_direction=flow_direction
        )
        return (
            elements,
            popovers,
            no_update,
            no_update,
            no_update,
            no_update
        )

    # Add Service Button
    if trigger_source == "button-add-service" and add_service_clicks > 0:
        elements, popovers = handle_add_service(
            elements=elements, popovers=popovers, id_index=add_service_clicks, flow_direction=flow_direction
        )
        return (

            elements,
            popovers,
            no_update,
            no_update,
            no_update,
            no_update
        )

    if trigger_source == "button-clean-pipeline":
        redis_instance.delete(session_id)
        return (
            [],
            [],
            no_update,
            no_update,
            no_update,
            [pipeline_controls, pipeline_chart]
        )

    if trigger_source == "button-pipeline-example":
        elements, popovers = create_pipeline_example(redis_instance=redis_instance, session_id=session_id)
        return (
            elements,
            popovers,
            no_update,
            no_update,
            no_update,
            no_update
        )

    if trigger_source == "flowchart" and connect_data:
        elements = handle_connect_data(elements=elements, connect_data=connect_data)
        return (
            elements,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )

    # Get changes on Dataset/Preprocessing/Model/Operation/Service select dropdowns
    if '"index":' in trigger_source:
        element_index = json.loads(trigger_source)["index"]
        name = ctx.triggered[0]["value"]
        if "dropdown-dataset" in trigger_source:
            element_type = "dataset"
        elif "dropdown-preprocessing" in trigger_source:
            element_type = "preprocessing"
        elif "dropdown-model" in trigger_source:
            element_type = "model"
        elif "dropdown-operation" in trigger_source:
            element_type = "operation"
        elif "dropdown-service" in trigger_source:
            element_type = "service"

        elements = update_elements_from_popovers(
            type=element_type, index=element_index, label=name, elements=elements
        )
        return (
            elements,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )

    return (
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update
    )


# Handle Dataset choice - within Popover
@app.callback(
    Output({"type": "div-popover-body-tabs-dataset", "index": MATCH}, "children"),
    [
        Input({"type": "div-popover-dropdown-dataset", "index": MATCH}, "value"),
        State("session-id", "data")
    ],
)
def handle_dataset_dropdown(dataset_name, session_id):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    # Choose Dataset Dropdown
    dataset_name = ctx.triggered[0]["value"]
    trigger_index = ctx.triggered[0]["prop_id"].split('index":')[1].split(",")[0]
    tabs = create_dataset_popover_body(dataset_name=dataset_name, redis_instance=redis_instance, index=trigger_index, session_id=session_id)

    return tabs


# Handle Preprocessing choice - within Popover
@app.callback(
    Output({"type": "div-popover-body-preprocessing", "index": MATCH}, "children"),
    [Input({"type": "div-popover-dropdown-preprocessing", "index": MATCH}, "value")],
)
def handle_preprocessing_dropdown(option):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    trigger_index = ctx.triggered[0]["prop_id"].split('index":')[1].split(",")[0]
    # Choose Preprocessing Dropdown
    preprocessing_name = ctx.triggered[0]["value"]

    body = create_preprocessing_popover_body(preprocessing_name, trigger_index)
    return body




# Handle Preprocessing Train/Test split slider
@app.callback(
    Output(
        {"type": "popover-body-preprocessing-slider-label", "index": MATCH}, "children"
    ),
    [Input({"type": "popover-body-preprocessing-slider", "index": MATCH}, "value")],
)
def handle_preprocessing_spliter(value):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    return f"Train: {value}%  |  Test: {100 - value}%"


# Handle Model choice - within Popover
@app.callback(
    Output({"type": "div-popover-body-model", "index": MATCH}, "children"),
    [Input({"type": "div-popover-dropdown-model", "index": MATCH}, "value")],
)
def handle_model_dropdown(model):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    # Choose Model Dropdown
    model_name = ctx.triggered[0]["value"]
    body = create_model_popover_body(model_name)

    return body


# Handle Operation choice - within Popover
@app.callback(
    Output({"type": "div-popover-body-operation", "index": MATCH}, "children"),
    [Input({"type": "div-popover-dropdown-operation", "index": MATCH}, "value")],
)
def handle_operation_dropdown(dataset_name):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    trigger_index = [p["prop_id"] for p in dash.callback_context.triggered][0]
    operation_name = ctx.triggered[0]["value"]

    body = create_operation_popover_body(
        operation_name=operation_name,
        index=trigger_index
    )

    return body


# Handle Service choice - within Popover
@app.callback(
    Output({"type": "div-popover-body-service", "index": MATCH}, "children"),
    [Input({"type": "div-popover-dropdown-service", "index": MATCH}, "value")],
)
def handle_service_dropdown(dataset_name):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    trigger_index = ctx.triggered[0]["prop_id"].split('index":')[1].split(",")[0]
    service_name = ctx.triggered[0]["value"]

    body = create_service_popover_body(
        service_name=service_name,
        index=trigger_index
    )
    return body


# Toggle flow direction
@app.callback(
    Output('flowdirection-store', 'data'),
    [Input("flowdirections-input", "value")],
    [State('flowdirection-store', 'data')]
)
def toggle_flow_direction(value, flowdirection):
    if value == 1:
        return "vertical"
    elif value == 2:
        return "horizontal"
    return no_update


# Tour control callback
@app.callback(
    Output("tour", "isOpen"),
    [Input("tour-btn", "n_clicks")],
)
def enable_intro(n_clicks):
    return n_clicks is not None and n_clicks > 0


# Toggle About Modal
@app.callback(
    Output("modal-about", "is_open"),
    Input("button-about", "n_clicks"),
    State("modal-about", "is_open"),
)
def toggle_about(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Close Popover Dataset
@app.callback(
    Output({"type": "popover-dataset", "index": MATCH}, "is_open"),
    [Input({"type": "popover-close-btn-dataset", "index": MATCH}, "n_clicks")],
    [State({"type": "popover-dataset", "index": MATCH}, "is_open")],
)
def close_popover_dataset(n_clicks, state):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    return not state


# Close Popover Preprocessing
@app.callback(
    Output({"type": "popover-preprocessing", "index": MATCH}, "is_open"),
    [Input({"type": "popover-close-btn-preprocessing", "index": MATCH}, "n_clicks")],
    [State({"type": "popover-preprocessing", "index": MATCH}, "is_open")],
)
def close_popover_preprocessing(n_clicks, state):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    return not state


# Close Popover Model
@app.callback(
    Output({"type": "popover-model", "index": MATCH}, "is_open"),
    [Input({"type": "popover-close-btn-model", "index": MATCH}, "n_clicks")],
    [State({"type": "popover-model", "index": MATCH}, "is_open")],
)
def close_popover_model(n_clicks, state):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    return not state


# Close Popover Operation
@app.callback(
    Output({"type": "popover-operation", "index": MATCH}, "is_open"),
    [Input({"type": "popover-close-btn-operation", "index": MATCH}, "n_clicks")],
    [State({"type": "popover-operation", "index": MATCH}, "is_open")],
)
def close_popover_operation(n_clicks, state):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    return not state


# Close Popover Service
@app.callback(
    Output({"type": "popover-service", "index": MATCH}, "is_open"),
    [Input({"type": "popover-close-btn-service", "index": MATCH}, "n_clicks")],
    [State({"type": "popover-service", "index": MATCH}, "is_open")],
)
def close_popover_service(n_clicks, state):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    return not state


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
    app.run_server(
        debug=True,
        # dev_tools_hot_reload=False
    )
