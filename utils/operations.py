import json
import time

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_design_kit as ddk
import numpy as np
import pandas as pd
from config import REDIS_EXPIRY
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)

from .figures import confusion_matrix_graph, roc_auc_graph


def run_compare_and_select(**kwargs):
    redis_instance = kwargs.get('redis_instance')
    session_id = kwargs.get('session_id')
    depends_on = kwargs.get('depends_on')
    element_id = kwargs.get('element_id')

    children = []
    rowData = []
    if isinstance(depends_on, list):
        for element in depends_on:
            redis_data = json.loads(redis_instance.hget(name=session_id, key=element))
            if "model" in element:
                y_pred = pd.read_json(redis_data["y_pred"], typ='series', orient='records')
                y_test = pd.read_json(redis_data["y_test"], typ='series', orient='records')
                y_scores = np.array(json.loads(redis_data["y_pred_proba"]))
                model_classes = np.array(json.loads(redis_data["model_classes"]))
                model_name = redis_data["model_name"]

                acc = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average="macro")
                precision = precision_score(y_test, y_pred, average="macro")
                recall= recall_score(y_test, y_pred, average="macro")

                cm = confusion_matrix(y_test, y_pred)

                model_info = {
                    "model": model_name,
                    "acc": acc.round(3),
                    "f1": f1.round(3),
                    "precision": precision.round(3),
                    "recall": recall.round(3)
                }

                rowData.append(model_info)
        
                tab = dbc.Tab(
                    label=model_name,
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    ddk.Graph(figure=roc_auc_graph(y_test, y_scores, model_classes)),
                                    md=6,
                                    lg=6,
                                    xl=6
                                ),
                                dbc.Col(
                                    ddk.Graph(figure=confusion_matrix_graph(cm, model_classes)),
                                    md=6,
                                    lg=6,
                                    xl=6
                                )
                            ]
                        )
                    ]
                )
                children.append(tab)

            else:
                raise KeyError('No model found!')
                
    else:
        redis_data = json.loads(redis_instance.hget(name=session_id, key=depends_on))
        if "model" in depends_on:
            y_pred = pd.read_json(redis_data["y_pred"], typ='series', orient='records')
            y_test = pd.read_json(redis_data["y_test"], typ='series', orient='records')
            y_scores = np.array(json.loads(redis_data["y_pred_proba"]))
            model_classes = np.array(json.loads(redis_data["model_classes"]))
            model_name = redis_data["model_name"]

            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="macro")
            precision = precision_score(y_test, y_pred, average="macro")
            recall= recall_score(y_test, y_pred, average="macro")

            cm = confusion_matrix(y_test, y_pred)

            model_info = {
                "model": model_name,
                "acc": acc.round(3),
                "f1": f1.round(3),
                "precision": precision.round(3),
                "recall": recall.round(3)
            }

            rowData.append(model_info)

            tab = dbc.Tab(
                label=model_name,
                children=[
                    dbc.Row(
                        [
                            dbc.Col(
                                ddk.Graph(figure=roc_auc_graph(y_test, y_scores, model_classes)),
                                md=6,
                                lg=6,
                                xl=6
                            ),
                            dbc.Col(
                                ddk.Graph(figure=confusion_matrix_graph(cm, model_classes)),
                                md=6,
                                lg=6,
                                xl=6
                            )
                        ]
                    )
                ]
            )
            children.append(tab)

        else:
            raise KeyError('No model found!')

    # Select the best model
    min_acc = 0
    best_model = {}
    for model in range(len(rowData)):
        if model == 0:
            min_acc = rowData[model]["acc"]
            best_model = rowData[model]
        else:
            if rowData[model]["acc"] < min_acc:
                min_acc = rowData[model]["acc"]
                best_model = rowData[model]

    # Save in Redis
    redis_instance.hset(
        name=session_id,
        key=element_id,
        value=json.dumps(best_model)
    )
    redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

    # Create table
    columnDefs = [
        {"headerName": "Model", "field": "model"},
        {"headerName": "Accuracy", "field": "acc"},
        {"headerName": "F1 Score", "field": "f1"},
        {"headerName": "Precision", "field": "precision"},
        {"headerName": "Recall", "field": "recall"},
    ]

    ag_grid = dag.AgGrid(
        columnDefs=columnDefs,
        rowData=rowData,
        defaultColDef=dict(
            resizable=True,
        )
    )

    compare_tab = dbc.Tab(
        label="Compare",
        children=[ag_grid]
    )
    children.insert(0, compare_tab)

    # Create children
    tabs = dbc.Tabs(
        children=children,
    )
    return tabs


def run_deploy(**kwargs):
    time.sleep(1)

    return 1


def run_report(**kwargs):
    time.sleep(1)

    return 1
