import json
import time

import pandas as pd
import plotly.express as px
from sklearn.datasets import load_breast_cancer, load_wine
from config import REDIS_EXPIRY


def run_load_dataset(**kwargs):
    '''
    Inputs:
        element_id: running node/step id
        redis_instance: Redis instance
        option: dataset name

    Output (Redis):
        {element_id: {"dataset": params["option"]}}
    '''
    time.sleep(1)

    redis_instance = kwargs.get('redis_instance')
    session_id = kwargs.get('session_id')
    element_id = kwargs.get('element_id')
    option = kwargs.get('option')

    if option == "iris":
        df = px.data.iris()
        df.rename(columns={"species": "class"}, inplace=True)
        redis_instance.hset(name=session_id, key="iris", value=df.to_json())
        redis_instance.hset(name=session_id, key=element_id, value=json.dumps({"dataset_name": option}))
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    elif option == "breast cancer":
        data = load_breast_cancer()
        x = data.data
        y = data.target

        df = pd.DataFrame(x, columns=data.feature_names)
        df = pd.concat([df, pd.Series(y, name="class")], axis=1)
        classes = {0: "malignant", 1: "benign"}
        df["class"] = df["class"].map(classes)

        del data
        redis_instance.hset(name=session_id, key="breast cancer", value=df.to_json())
        redis_instance.hset(name=session_id, key=element_id, value=json.dumps({"dataset_name": option}))
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    elif option == "wine":
        data = load_wine()
        x = data.data
        y = data.target

        df = pd.DataFrame(x, columns=data.feature_names)
        df = pd.concat([df, pd.Series(y, name="class", dtype=str)], axis=1)
        del data

        redis_instance.hset(name=session_id, key="wine", value=df.to_json())
        redis_instance.hset(name=session_id, key=element_id, value=json.dumps({"dataset_name": option}))
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    else:
        raise ValueError('No dataset was selected!')


def run_train_test_split(**kwargs):
    '''
    Inputs:
        depends_on: id of the previous process (needed to get the data in Redis)
        element_id: running node/step id
        extra_args: train_size
        redis_instance: Redis instance

    Output (Redis):
        {element_id: {"train_data": train_data,
                      "test_data": test_data}}
    '''
    time.sleep(1)

    redis_instance = kwargs.get('redis_instance')
    session_id = kwargs.get('session_id')
    depends_on = kwargs.get('depends_on')
    element_id = kwargs.get('element_id')
    train_size = kwargs.get("extra_args")/100

    # TODO check if will stay hardcoded
    target_column = "class"

    redis_data = json.loads(redis_instance.hget(name=session_id, key=depends_on))
    if next(iter(redis_data)) == "dataset_name":
        df = pd.read_json(redis_instance.hget(name=session_id, key=redis_data["dataset_name"]))
        X_data, y_data = df.drop(target_column, axis=1), df[target_column]

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data,
                                                            train_size=train_size)

        X_train[target_column] = y_train
        X_test[target_column] = y_test

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({
                "train_data": X_train.to_json(),
                "test_data": X_test.to_json()
            })
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    elif next(iter(redis_data)) == "dataframe":
        df = pd.read_json(redis_data["dataframe"])
        X_data, y_data = df.drop(target_column, axis=1), df[target_column]

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data,
                                                            train_size=train_size)

        X_train[target_column] = y_train
        X_test[target_column] = y_test

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({
                "train_data": X_train.to_json(),
                "test_data": X_test.to_json()
            })
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

        return 1

    else:
        raise KeyError('No dataframe found!')


def run_replace_nan(**kwargs):
    '''
    Inputs:
        depends_on: id of the previous process (needed to get the data in Redis)
        element_id: running node/step id
        redis_instance: Redis instance

    Output (Redis) if input is dataset:
        {element_id: {"dataframe": df}}

    Output (Redis) if input is X_train, X_test, y_train, y_test:
        {element_id: {"train_data": train_data,
                      "test_data": test_data}}
    '''
    time.sleep(1)

    redis_instance = kwargs.get('redis_instance')
    session_id = kwargs.get('session_id')
    depends_on = kwargs.get('depends_on')
    element_id = kwargs.get('element_id')

    redis_data = json.loads(redis_instance.hget(name=session_id, key=depends_on))
    if next(iter(redis_data)) == "dataset_name":
        df = pd.read_json(redis_instance.hget(name=session_id, key=redis_data["dataset_name"]))
        df.dropna(inplace=True)

        redis_instance.hset(name=session_id, key=element_id, value=json.dumps({"dataframe": df.to_json()}))
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

    if next(iter(redis_data)) == "dataframe":
        df = pd.read_json(redis_data["dataframe"])
        df.dropna(inplace=True)

        redis_instance.hset(name=session_id, key=element_id, value=json.dumps({"dataframe": df.to_json()}))
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

    if next(iter(redis_data)) == "train_data":
        train_data = pd.read_json(redis_data["train_data"])
        test_data = pd.read_json(redis_data["test_data"])

        train_data.dropna(inplace=True)
        test_data.dropna(inplace=True)

        redis_instance.hset(
            name=session_id,
            key=element_id,
            value=json.dumps({
                "train_data": train_data.to_json(),
                "test_data": test_data.to_json()
            })
        )
        redis_instance.expire(name=session_id, time=REDIS_EXPIRY)

    return 1


def run_one_hot_encoding(**kwargs):
    time.sleep(1)

    return 1


def run_normalize(**kwargs):
    time.sleep(1)

    return 1


def run_log_transform(**kwargs):
    time.sleep(1)

    return 1
