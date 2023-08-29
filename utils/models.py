import json
import time

import pandas as pd
from config import REDIS_EXPIRY


def run_xgboost(**kwargs):
    '''
    Inputs:
        depends_on: id of the previous process (needed to get the data in Redis)
        element_id: running node/step id
        params: {"target": "target column"}
        redis_instance: Redis instance

    Output (Redis):
        {element_id: {"model": model.pkl}}
    '''

    redis_instance = kwargs.get('redis_instance')
    session_id = kwargs.get('session_id')
    depends_on = kwargs.get('depends_on')
    element_id = kwargs.get('element_id')

    # TODO check if will stay hardcoded
    target_column = "class"

    redis_data = json.loads(redis_instance.hget(name=session_id, key=depends_on))
    if next(iter(redis_data)) == "dataset_name":
        df = pd.read_json(redis_instance.hget(name=session_id, key=redis_data["dataset_name"]))
        X_data, y_data = df.drop(target_column, axis=1), df[target_column]

        from xgboost import XGBClassifier
        model = XGBClassifier().fit(X_data, y_data)

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({"model": "xgboost"})
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    elif next(iter(redis_data)) == "dataframe":
        df = pd.read_json(redis_data["dataframe"])
        X_data, y_data = df.drop(target_column, axis=1), df[target_column]

        from xgboost import XGBClassifier
        model = XGBClassifier().fit(X_data, y_data)

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({"model": "xgboost"})
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    elif next(iter(redis_data)) == "train_data":
        from xgboost import XGBClassifier
        train_data = pd.read_json(redis_data["train_data"])
        X_train, y_train = train_data.drop(target_column, axis=1), train_data[target_column]
        test_data = pd.read_json(redis_data["test_data"])
        X_test, y_test = test_data.drop(target_column, axis=1), test_data[target_column]
        model = XGBClassifier().fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)

        redis_instance.hset(
            name=session_id,
            key=element_id, 
            value=json.dumps({
                "y_pred": pd.Series(y_pred).to_json(),
                "y_test": pd.Series(y_test).to_json(),
                "y_pred_proba": json.dumps(y_pred_proba.tolist()),
                "model_classes": json.dumps(model.classes_.tolist()),
                "model_name": "XGBoost"
            })
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    else:
        raise KeyError('No data found!')


def run_log_classifier(**kwargs):
    '''
    Inputs:
        depends_on: id of the previous process (needed to get the data in Redis)
        element_id: running node/step id
        params: {"target": "target column"}
        redis_instance: Redis instance

    Output (Redis):
        {element_id: {"model": model.pkl}}
    '''

    redis_instance = kwargs.get('redis_instance')
    session_id = kwargs.get('session_id')
    depends_on = kwargs.get('depends_on')
    element_id = kwargs.get('element_id')

    # TODO check if will stay hardcoded
    target_column = "class"

    redis_data = json.loads(redis_instance.hget(name=session_id, key=depends_on))
    if next(iter(redis_data)) == "dataset_name":
        df = pd.read_json(redis_instance.hget(name=session_id, key=redis_data["dataset_name"]))
        X_data, y_data = df.drop(target_column, axis=1), df[target_column]

        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression().fit(X_data, y_data)

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({"model": "xgboost"})
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    elif next(iter(redis_data)) == "dataframe":
        df = pd.read_json(redis_data["dataframe"])
        X_data, y_data = df.drop(target_column, axis=1), df[target_column]

        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression().fit(X_data, y_data)

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({"model": "xgboost"})
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    elif next(iter(redis_data)) == "train_data":
        from sklearn.linear_model import LogisticRegression
        train_data = pd.read_json(redis_data["train_data"])
        X_train, y_train = train_data.drop(target_column, axis=1), train_data[target_column]
        test_data = pd.read_json(redis_data["test_data"])
        X_test, y_test = test_data.drop(target_column, axis=1), test_data[target_column]
        model = LogisticRegression().fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({
                "y_pred": pd.Series(y_pred).to_json(),
                "y_test": pd.Series(y_test).to_json(),
                "y_pred_proba": json.dumps(y_pred_proba.tolist()),
                "model_classes": json.dumps(model.classes_.tolist()),
                "model_name": "Logistic Classifier"
            })
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1
    
    else:
        raise KeyError('No data found!')


def run_kmeans(**kwargs):
    time.sleep(1)

    return 1


def run_deep_classifier(**kwargs):
    time.sleep(1)

    return 1


def run_automl_classifier(**kwargs):
    time.sleep(1)

    return 1