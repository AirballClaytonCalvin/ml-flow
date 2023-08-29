from dash import html, dcc, no_update
import dash_bootstrap_components as dbc
import dash_design_kit as ddk
import redis
import dash_pro_components as pro
import dash_ag_grid as dag
from sklearn.datasets import load_breast_cancer, load_wine
import plotly.express as px
import pandas as pd
import time
from .functions_mapping import FUNCTIONS_MAP, STRING_TO_FUNCTION_MAPPING
from config import REDIS_EXPIRY


def update_node_layout(node, elements):

    # clean all nodes background styles
    cancel_pipeline = False
    for e in elements:
        if e["id"].startswith("edge"):
            continue
        my_style = e["data"].get("style", {})
        if my_style.get("backgroundColor", False) and e['id'] != node['id']:
            del e['data']['style']['backgroundColor']
        elif e['id'] == node['id']:
            if not node['data'].get('description', False):
                cancel_pipeline = True
                my_style["backgroundColor"] = "#ff9e9e"
            else:
                my_style["backgroundColor"] = "#a8ffa5"
            node['data']['style'] = my_style

    return cancel_pipeline, elements


def process_pipeline_step(step, redis_instance, session_id):
    """ """
    func_name = step.get('function', False)
    time.sleep(1)
    if not func_name:
        return
    time.sleep(1)
    print(f'Running function {func_name}')
    func = STRING_TO_FUNCTION_MAPPING[func_name]
    args = {
        "depends_on": step.get('depends_on'),
        "element_id": step.get('element_id'),
        "option": step.get('option'),
        "extra_args": step.get('parameters'),
        "redis_instance": redis_instance,
        "session_id": session_id
    }

    # Execute function
    step_results = func(**args)

    return step_results


def handle_connect_data(elements, connect_data):
    """ """
    for e in elements:
        if e == connect_data:
            if "handle-train" in e["sourceHandle"]:
                e["label"] = "Train Data"
            elif "handle-test" in e["sourceHandle"]:
                e["label"] = "Test Data"

    return elements


def create_dag(
    elements=None,
    dag=None,
    edge_elements=None,
    data_elements=None,
    root=None,
    level=0,
    params=None
):
    """Create dag from elements list (nodes and edges)"""
    global FUNCTIONS_MAP
    if dag is None:
        dag = dict()

    if level == 0:
        edge_elements = [e for e in elements if e["id"].startswith("edge")]
        data_elements = [e for e in elements if not e["id"].startswith("edge")]
        roots = list()
        dag[level] = list()
        for e in data_elements:
            if e["type"] == "customInput" or e["type"] == "input":
                flow_direction = 'vertical' if e['sourcePosition'] == 'bottom' else 'horizontal'
                roots.append(e["id"])
                dag[level].append(
                    {
                        'depends_on': None,
                        'element_id': e['id'],
                        'status': 'wating',
                        'type': 'dataset',
                        'option': e['data']['label'].lower(),
                        'function': FUNCTIONS_MAP['dataset'], # TODO add py function here
                        'parameters': params.get(e['id'], None), # TODO add kwargs as dict to input directly in function using -> func(**{'type':'Event'})
                        'position': e['position'],
                        'flow_direction': flow_direction
                    }
                )
                #dag[level].append((None, e["id"]))

        if not roots:
            return {}

        return create_dag(
            dag=dag,
            edge_elements=edge_elements,
            data_elements=data_elements,
            root=roots,
            level=1,
            params=params
        )

    if level not in dag:
        dag[level] = list()

    new_root = list()
    elements_to_remove = list()
    target_elements = list()
    for e in edge_elements:
        if e['target'] not in target_elements:
            for r in root:
                if e['source'] == r:
                    data_element = [el for el in data_elements if e['target'] == el['id']][0]
                    data_type = data_element['data'].get('description', None)
                    if data_type is not None:
                        data_type = data_type.split(':')[0].lower()
                    data_option = data_element['data']['label'].lower()
                    function = FUNCTIONS_MAP.get(data_type, None)
                    if function is not None:
                        function = function.get(data_option, None)

                    flow_direction = 'vertical' if data_element['targetPosition'] == 'top' else 'horizontal'
                    step = {
                        'depends_on': e['source'],
                        'element_id': data_element['id'],
                        'status': 'wating',
                        'type': data_type,
                        'option': data_option,
                        'function': function,
                        'parameters': params.get(data_element['id'], None), # TODO add kwargs as dict to input directly in function using -> func(**{'type':'Event'})
                        'position': data_element['position'],
                        'flow_direction': flow_direction
                    }

                    if step not in dag[level]: 
                        dag[level].append(step)
            target_elements.append(e['target'])

        elif e['target'] in target_elements:
            for step in dag[level]:
                if step['element_id'] == e['target']:
                    step['depends_on'] = root if len(root) > 1 else root[0]

    # Remove already used elements
    for e in edge_elements:
        if e["source"] in root:
            new_root.append(
                e["target"]
            )  # append id of target elements to new root (change level)
            elements_to_remove.append(e)

    # Remove already used elements
    for e in elements_to_remove:
        if e in edge_elements:
            edge_elements.remove(e)

    # If all elements were removed, stop recursion
    if not edge_elements:
        return dag

    level += 1
    return create_dag(
        dag=dag, edge_elements=edge_elements, data_elements=data_elements, root=new_root, level=level, params=params
    )


def update_elements_from_popovers(type, index, label, elements):
    """ """
    for i, e in enumerate(elements):
        if e["id"] == index:
            e["data"]["label"] = label
            e["data"]["description"] = "{}: {}".format(type.title(), label)
            e["data"]["sourceHandleNumber"] = 1
            elements[i] = e
            return elements
    return elements


def handle_add_dataset(elements, popovers, id_index, position=None, flow_direction=None, **kwargs):
    """Generate nodes elements for dataset"""

    if position is None:
        position = {"x": 250, "y": 25}

    if flow_direction is None:
        flow_direction = 'vertical'

    # New Node
    new_element = {
        "id": f"node-element-dataset-{id_index}",
        "type": "customInput",  # input node - dataset
        "data": {
            "label": "Dataset",
            "style": {
                "borderWidth": "2px",
                "borderColor": "#008000",
            },
            "useIcon": True,
            "iconId": f"icon-dataset-{id_index}",
            "iconClassName": "fas fa-database",
            "iconStyle": {"cursor": "pointer"}
        },
        "position": position,
        "targetPosition": ["top" if flow_direction == "vertical" else "left"][0],
        "sourcePosition": ["bottom" if flow_direction == "vertical" else "right"][0],
    }
    elements.append(new_element)

    popover_body = kwargs.get('popover_body', [])
    # Popover
    popover_body = html.Div(
        id={"type": "div-popover-body-tabs-dataset", "index": f"node-element-dataset-{id_index}"},
        children=popover_body
    )

    select = dbc.Select(
        placeholder="Choose Dataset",
        id={"type": "div-popover-dropdown-dataset", "index": f"node-element-dataset-{id_index}"},
        options=[
            {"label": "Iris", "value": "Iris"},
            {"label": "Wine", "value": "Wine"},
            {"label": "Breast Cancer", "value": "Breast Cancer"},
            {"label": "Upload CSV", "value": "Upload CSV", "disabled": True},
        ],
        style={
            "minWidth": "230px",
            "maxWidth": "230px",
        },
    )

    popovers.append(
        ddk.Block(
            dbc.Popover(
                [
                    dbc.PopoverHeader(
                        ddk.Row(
                            [
                                html.Button(
                                    html.I(className="far fa-times-circle"),
                                    id={
                                        "type": "popover-close-btn-dataset",
                                        "index": f"node-element-dataset-{id_index}",
                                    },
                                    style={
                                        "backgroundColor": "transparent",
                                        "borderColor": "transparent",
                                        "minWidth": "40px",
                                        "maxWidth": "40px",
                                    },
                                ), 
                                select, 
                            ],
                        )
                    ),
                    dbc.PopoverBody(
                        children=[popover_body],
                        id={"type": "popover-body-dataset", "index": f"node-element-dataset-{id_index}"},
                    ),
                ],
                id={"type": "popover-dataset", "index": f"node-element-dataset-{id_index}"},
                target=f"icon-dataset-{id_index}",
                #target=f"node-element-dataset-{id_index}",
                # target={'type':'node-element-dataset','index':id_index},
                placement="bottom",
                is_open=False,
                trigger="click",
            )
        )
    )
    return elements, popovers


def handle_add_preprocessing(elements, popovers, id_index, position=None, flow_direction=None, **kwargs):
    """Generate nodes elements for preprocessing"""
    if position is None:
        position = {"x": 250, "y": 25}

    if flow_direction is None:
        flow_direction = 'vertical'

    # New Node
    new_element = {
        # "id": f"{{'type':'node-element-preprocessing','index':{id_index}}}",
        "id": f"node-element-preprocessing-{id_index}",
        "type": "customDefault",
        "data": {
            "label": "Preprocessing",
            "style": {"borderRadius": "0", "borderColor": "gray"},
            "useIcon": True,
            "iconId": f"icon-preprocessing-{id_index}",
            "iconClassName": "fas fa-wave-square",
            "iconStyle": {"cursor": "pointer"}
        },
        "targetPosition": ["top" if flow_direction == "vertical" else "left"][0],
        "sourcePosition": ["bottom" if flow_direction == "vertical" else "right"][0],
        "position": position,
    }
    elements.append(new_element)

    # Popover
    preprocessing_select = dbc.Select(
        id={"type": "div-popover-dropdown-preprocessing", "index": f"node-element-preprocessing-{id_index}"},
        placeholder="Choose Preprocessing",
        options=[
            {"label": "Train/Test split", "value": "Train/Test split"},
            {"label": "NaN replacing", "value": "NaN replacing", "disabled": True},
            {"label": "One-hot encoding", "value": "One-hot encoding", "disabled": True},
            {"label": "Normalization", "value": "Normalization", "disabled": True},
            {"label": "Log-transform", "value": "Log-transform", "disabled": True},
        ],
        style={
            "minWidth": "230px",
            "maxWidth": "230px",
        },
    )

    popover_body = kwargs.get('popover_body', [])
    popover_body_content = html.Div(
        id={"type": "div-popover-body-preprocessing", "index": f"node-element-preprocessing-{id_index}"},
        children=popover_body
    )

    new_popover = dbc.Popover(
        [
            dbc.PopoverHeader(
                ddk.Row(
                    [
                        html.Button(
                            html.I(className="far fa-times-circle"),
                            id={
                                "type": "popover-close-btn-preprocessing",
                                "index": f"node-element-preprocessing-{id_index}",
                            },
                            style={
                                "backgroundColor": "transparent",
                                "borderColor": "transparent",
                                "minWidth": "40px",
                                "maxWidth": "40px",
                            },
                        ),
                        preprocessing_select,
                    ]
                )
            ),
            dbc.PopoverBody(
                children=[popover_body_content],
                id={"type": "popover-body-preprocessing", "index": f"node-element-preprocessing-{id_index}"},
            ),
        ],
        id={"type": "popover-preprocessing", "index": f"node-element-preprocessing-{id_index}"},
        target=f"icon-preprocessing-{id_index}",
        # target={'type':'node-element-preprocessing','index':id_index},
        placement="bottom",
        is_open=False,
        trigger="click",
    )
    popovers.append(new_popover)

    return elements, popovers


def handle_add_model(elements, popovers, id_index, position=None, flow_direction=None, **kwargs):
    """Generate nodes elements for models"""
    if position is None:
        position = {"x": 250, "y": 25}

    if flow_direction is None:
        flow_direction = 'vertical'

    # New Node
    pattern_match_id = f'{{"index":{id_index},"type":"node-element-model"}}'
    new_element = {
        "id": f"node-element-model-{id_index}",
        "type": "customDefault",
        "data": {
            "label": "Model",
            "pattern_match_id": pattern_match_id,
            "style": {
                "borderRadius": "5rem",
                "borderColor": "black",
                "borderWidth": "2px",
            },
            "useIcon": True,
            "iconId": f"icon-model-{id_index}",
            "iconClassName": "fas fa-network-wired",
            "iconStyle": {"cursor": "pointer"}
        },
        "position": position,
        "targetPosition": ["top" if flow_direction == "vertical" else "left"][0],
        "sourcePosition": ["bottom" if flow_direction == "vertical" else "right"][0],
    }
    elements.append(new_element)

    # Popover
    select = dbc.Select(
        id={"type": "div-popover-dropdown-model", "index": f"node-element-model-{id_index}"},
        placeholder="Choose Model",
        options=[
            {"label": "Logistic Classifier", "value": "Logistic Classifier"},
            {"label": "XGBoost", "value": "XGBoost"},
            {"label": "KMeans", "value": "KMeans", "disabled": True},
            {"label": "Deep Classifier", "value": "Deep Classifier", "disabled": True},
            {"label": "AutoML Classifier", "value": "AutoML Classifier", "disabled": True},
        ],
        style={
            "minWidth": "230px",
            "maxWidth": "230px",
        },
    )

    popover_body = kwargs.get('popover_body', [])
    popover_body_content = html.Div(
        id={"type": "div-popover-body-model", "index": f"node-element-model-{id_index}"},
        children=popover_body
    )

    new_popover = dbc.Popover(
        [
            dbc.PopoverHeader(
                ddk.Row(
                    [
                        html.Button(
                            html.I(className="far fa-times-circle"),
                            id={"type": "popover-close-btn-model", "index": f"node-element-model-{id_index}"},
                            style={
                                "backgroundColor": "transparent",
                                "borderColor": "transparent",
                                "minWidth": "40px",
                                "maxWidth": "40px",
                            },
                        ),
                        select,
                    ]
                )
            ),
            dbc.PopoverBody(
                children=[popover_body_content],
                id={"type": "popover-body-model", "index": f"node-element-model-{id_index}"},
            ),
        ],
        id={"type": "popover-model", "index": f"node-element-model-{id_index}"},
        target=f"icon-model-{id_index}",
        # target={'type':'node-element-model','index':id_index},
        placement="bottom",
        is_open=False,
        trigger="click",
    )
    popovers.append(new_popover)

    return elements, popovers


def handle_add_operation(elements, popovers, id_index, position=None, flow_direction=None, **kwargs):
    """Generate nodes elements for operations"""
    if position is None:
        position = {"x": 250, "y": 25}

    if flow_direction is None:
        flow_direction = 'vertical'

    # New Node
    new_element = {
        # "id": f"{{'type':'node-element-operation','index':{id_index}}}",
        "id": f"node-element-operation-{id_index}",
        "type": "customDefault",
        "data": {
            "label": "Operation",
            # "targetHandleNumber": 3,
            # "targetHandleIds": ["handle-ops-1", 'handle-ops-2', 'handle-ops-3'],
            "style": {
                "borderRadius": "0",
                "borderColor": "black",
                "borderStyle": "dotted",
                "borderWidth": "1px",
            },
            "useIcon": True,
            "iconId": f"icon-operation-{id_index}",
            "iconClassName": "fas fa-calculator",
            "iconStyle": {"cursor": "pointer"}
        },
        "position": position,
        "targetPosition": ["top" if flow_direction == "vertical" else "left"][0],
        "sourcePosition": ["bottom" if flow_direction == "vertical" else "right"][0],
    }
    elements.append(new_element)

    # Popover
    select = dbc.Select(
        id={"type": "div-popover-dropdown-operation", "index": f"node-element-operation-{id_index}"},
        placeholder="Choose Operation",
        options=[
            {"label": "Compare & Select", "value": "Compare & Select"},
            {"label": "Custom Function", "value": "Custom Function"},
        ],
        style={
            "minWidth": "230px",
            "maxWidth": "230px",
        },
    )

    popover_body = kwargs.get('popover_body', [])
    popover_body_content = html.Div(
        id={"type": "div-popover-body-operation", "index": f"node-element-operation-{id_index}"},
        children=popover_body
    )

    new_popover = dbc.Popover(
        [
            dbc.PopoverHeader(
                ddk.Row(
                    [
                        html.Button(
                            html.I(className="far fa-times-circle"),
                            id={
                                "type": "popover-close-btn-operation",
                                "index": f"node-element-operation-{id_index}",
                            },
                            style={
                                "backgroundColor": "transparent",
                                "borderColor": "transparent",
                                "minWidth": "40px",
                                "maxWidth": "40px",
                            },
                        ),
                        select,
                    ]
                )
            ),
            dbc.PopoverBody(
                children=[popover_body_content],
                id={"type": "popover-body-operation", "index": f"node-element-operation-{id_index}"},
            ),
        ],
        id={"type": "popover-operation", "index": f"node-element-operation-{id_index}"},
        target=f"icon-operation-{id_index}",
        # target={'type':'node-element-operation','index':id_index},
        placement="bottom",
        is_open=False,
        trigger="click",
    )
    popovers.append(new_popover)

    return elements, popovers


def handle_add_service(elements, popovers, id_index, position=None, flow_direction=None, **kwargs):
    """Generate nodes elements for services"""
    if position is None:
        position = {"x": 250, "y": 25}

    if flow_direction is None:
        flow_direction = 'vertical'

    # New Node
    new_element = {
        # "id": f"{{'type':'node-element-service','index':{id_index}}}",
        "id": f"node-element-service-{id_index}",
        "type": "customOutput",
        "data": {
            "label": "Service",
            "style": {
                "borderRadius": "10rem",
                "borderWidth": "2px",
            },
            "useIcon": True,
            "iconId": f"icon-service-{id_index}",
            "iconClassName": "fas fa-cloud-upload-alt",
            "iconStyle": {"cursor": "pointer"}
        },
        "position": position,
        "targetPosition": ["top" if flow_direction == "vertical" else "left"][0],
        "sourcePosition": ["bottom" if flow_direction == "vertical" else "right"][0],
    }
    elements.append(new_element)

    # Popover
    select = dbc.Select(
        id={"type": "div-popover-dropdown-service", "index": f"node-element-service-{id_index}"},
        placeholder="Choose Service",
        options=[
            {"label": "Deploy", "value": "Deploy"},
            {"label": "Report", "value": "Report"},
        ],
        style={
            "minWidth": "230px",
            "maxWidth": "230px",
        },
    )

    popover_body = kwargs.get('popover_body', [])
    popover_body_content = html.Div(
        id={"type": "div-popover-body-service", "index": f"node-element-service-{id_index}"},
        children=popover_body
    )

    new_popover = dbc.Popover(
        [
            dbc.PopoverHeader(
                ddk.Row(
                    [
                        html.Button(
                            html.I(className="far fa-times-circle"),
                            id={"type": "popover-close-btn-service", "index": f"node-element-service-{id_index}"},
                            style={
                                "backgroundColor": "transparent",
                                "borderColor": "transparent",
                                "minWidth": "40px",
                                "maxWidth": "40px",
                            },
                        ),
                        select,
                    ]
                )
            ),
            dbc.PopoverBody(
                children=[popover_body_content],
                id={"type": "popover-body-service", "index": f"node-element-service-{id_index}"},
            ),
        ],
        id={"type": "popover-service", "index": f"node-element-service-{id_index}"},
        target=f"icon-service-{id_index}",
        # target={'type':'node-element-service','index':id_index},
        placement="bottom",
        is_open=False,
        trigger="click",
    )
    popovers.append(new_popover)

    return elements, popovers


def load_dataset(dataset, redis_instance, session_id):
    """Load Dataset to store"""
    if dataset is None:
        return None

    if dataset.lower() == "iris":
        # data = load_iris()
        # df = pd.DataFrame(data.data, columns=data.feature_names)
        df = px.data.iris()
        df.rename(columns={"species": "class"}, inplace=True)
        fig = px.scatter(df, x="sepal_width", y="sepal_length", color="class")
        redis_instance.hset(name=session_id, key="iris", value=df.to_json())
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return df, fig
    elif dataset.lower() == "breast cancer":
        data = load_breast_cancer()
        x = data.data
        y = data.target

        df = pd.DataFrame(x, columns=data.feature_names)
        df = pd.concat([df, pd.Series(y, name="class")], axis=1)
        classes = {0: "malignant", 1: "benign"}
        df["class"] = df["class"].map(classes)
        fig = px.scatter(df, x="texture error", y="mean radius", color="class")
        del data
        redis_instance.hset(name=session_id, key="breast cancer", value=df.to_json())
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return df, fig
    elif dataset.lower() == "wine":
        data = load_wine()
        x = data.data
        y = data.target

        df = pd.DataFrame(x, columns=data.feature_names)
        df = pd.concat([df, pd.Series(y, name="class", dtype=str)], axis=1)
        del data
        fig = px.scatter(df, x="color_intensity", y="total_phenols", color="class")
        redis_instance.hset(name=session_id, key="wine", value=df.to_json())
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)
        return df, fig

    return None


def create_dataset_popover_body(dataset_name, redis_instance, index, session_id):
    df, fig = load_dataset(dataset=dataset_name, redis_instance=redis_instance, session_id=session_id)
    if df is None:
        return no_update

    columnDefs = [
        {
            "field": column,
            "sortable": True,
            "filter": True,
            "rowGroup": [True if column == "class" else False][0],
            "checkboxSelection": False,
            "headerCheckboxSelection": False,
        }
        for column in df.columns
    ]
    table_data = df.to_dict("records")
    ag_grid = dag.AgGrid(
        columnDefs=columnDefs,
        rowData=table_data,
        style={"min-width": "50vw", "height": "400px", "padding": "1rem"},
        rowSelection="multiple",
        # columnSize="sizeToFit",
        defaultColDef=dict(
            resizable=True,
        ),
        enableEnterpriseModules=True,
        licenseKey="LICENSE_KEY_HERE",
    )

    graph = ddk.Graph(
        figure=fig, style={"min-width": "50vw", "height": "400px", "padding": "1rem"}
    )

    tabs = dbc.Tabs(
        id={"type": "popover-body-dataset-tabs-tab", "index": index},
        children=[
            dbc.Tab(label="Table", children=[ag_grid]),
            dbc.Tab(label="Plots", children=[graph]),
        ],
    )

    return tabs


def create_preprocessing_popover_body(preprocessing_name, index, train_size=80):
    if preprocessing_name.lower() == "train/test split":
        component = html.Div(
            children=[
                dbc.Label(
                    id={
                        "type": "popover-body-preprocessing-slider-label",
                        "index": index.replace("'", '').replace('"', ''),
                    },
                    children=[f"Train: {train_size}%  |  Test: {100-train_size}%"],
                ),
                dcc.Slider(
                    id={
                        "type": "popover-body-preprocessing-slider",
                        "index": index.replace("'", '').replace('"', ''),
                    },
                    min=1,
                    max=99,
                    step=1,
                    value=train_size,
                ),
            ],
            style={"padding-top": "1rem"},
        )
        return component

    else:
        return html.H3(preprocessing_name.capitalize())


def create_model_popover_body(model_name):
    return html.H3(model_name.capitalize())


def create_operation_popover_body(operation_name, index):
    if operation_name.lower() != 'custom function':
        return html.H3(operation_name.capitalize())

    component = html.Div(
        children=[
            pro.CodeAce(
                fontSize=14,
                theme='github'
            )
        ]
    )
    return component


def create_service_popover_body(service_name, index, value=None):
    if service_name.lower() == "deploy":
        component = html.Div(
            children=[
                dbc.Label("Deploy to:"),
                dbc.Checklist(
                    id={
                        "type": "popover-service-deploy-checklist",
                        "index": index.replace('"', '').replace("'", ''),
                    },
                    options=[
                        {"label": "AWS", "value": 1},
                        {"label": "Azure", "value": 2},
                        {"label": "GCP", "value": 3},
                    ],
                    value=[] if value is None else value,
                    label_checked_style={"color": "red"},
                ),
            ]
        )
        return component

    if service_name.lower() == "report":
        component = html.Div(
            children=[
                dbc.Label("Email: "),
                dbc.Input(
                    id={
                        "type": "popover-service-email",
                        "index": index.replace('"', '').replace("'", '')
                    },
                    value=value,
                    placeholder="enter email address",
                    className="mb-3",
                ),
            ]
        )
        return component

    return no_update


def dag_to_elements(dag, redis_instance, session_id):
    flowchart_children = []
    popover_children = []

    for k, v in dag.items():
        for e in v:
            # Create nodes and popovers data
            if e['type'] == 'dataset':
                popover_body = create_dataset_popover_body(
                    dataset_name=e['option'],
                    redis_instance=redis_instance,
                    session_id=session_id,
                    index=e['element_id'],
                )
                flowchart_children, popover_children = handle_add_dataset(
                    elements=flowchart_children,
                    popovers=popover_children,
                    id_index=e['element_id'].split('-')[-1],
                    popover_body=popover_body,
                    position=e['position'],
                    flow_direction=e['flow_direction']
                )
            if e['type'] == 'preprocessing':
                popover_body = create_preprocessing_popover_body(
                    preprocessing_name=e['option'],
                    index=e['element_id'],
                    train_size=e['parameters'] if e['parameters'] else None
                )
                flowchart_children, popover_children = handle_add_preprocessing(
                    elements=flowchart_children,
                    popovers=popover_children,
                    id_index=e['element_id'].split('-')[-1],
                    position=e['position'],
                    popover_body=popover_body,
                    flow_direction=e['flow_direction']
                )
            if e['type'] == 'model':
                popover_body = create_model_popover_body(
                    model_name=e['option']
                )
                flowchart_children, popover_children = handle_add_model(
                    elements=flowchart_children,
                    popovers=popover_children,
                    id_index=e['element_id'].split('-')[-1],
                    position=e['position'],
                    popover_body=popover_body,
                    flow_direction=e['flow_direction']
                )
            if e['type'] == 'operation':
                popover_body = create_operation_popover_body(
                    operation_name=e['option'],
                    index=e['element_id'],
                )
                flowchart_children, popover_children = handle_add_operation(
                    elements=flowchart_children,
                    popovers=popover_children,
                    id_index=e['element_id'].split('-')[-1],
                    position=e['position'],
                    popover_body=popover_body,
                    flow_direction=e['flow_direction']
                )
            if e['type'] == 'service':
                popover_body = create_service_popover_body(
                    service_name=e['option'],
                    index=e['element_id'],
                    value=e['parameters']
                )
                flowchart_children, popover_children = handle_add_service(
                    elements=flowchart_children,
                    popovers=popover_children,
                    id_index=e['element_id'].split('-')[-1],
                    position=e['position'],
                    popover_body=popover_body,
                    flow_direction=e['flow_direction']
                )
            flowchart_children = update_elements_from_popovers(
                type=e['type'],
                index=e['element_id'],
                label=e['option'].capitalize(),
                elements=flowchart_children,
            )
            # Add edges
            if isinstance(e['depends_on'], list):
                for dependency in e['depends_on']:
                    edge_element = {
                        'source': dependency,
                        'target': e['element_id'],
                        'id': 'edge-{source_id}-{target_id}'.format(
                            source_id=dependency,
                            target_id=e['element_id']
                        )
                    }
                    flowchart_children.append(edge_element)
            elif isinstance(e['depends_on'], str):
                edge_element = {
                        'source': e['depends_on'],
                        'target': e['element_id'],
                        'id': 'edge-{source_id}-{target_id}'.format(
                            source_id=e['depends_on'],
                            target_id=e['element_id']
                        )
                    }
                flowchart_children.append(edge_element)

    return flowchart_children, popover_children
