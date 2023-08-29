from .models import (
    run_kmeans,
    run_log_classifier,
    run_xgboost,
    run_deep_classifier,
    run_automl_classifier,
)

from .preprocessing import (
    run_load_dataset,
    run_train_test_split,
    run_replace_nan,
    run_normalize,
    run_one_hot_encoding,
    run_log_transform
)

from .operations import (
    run_compare_and_select,
    run_deploy,
    run_report
)

FUNCTIONS_MAP = {
    "dataset": "run_load_dataset",
    "preprocessing": {
        "train/test split": "run_train_test_split",
        "normalization": "run_normalize",
        "nan replacing": "run_replace_nan",
        "one-hot encoding": "run_one_hot_encoding",
        "log-transform": "run_log_transform"
    },
    "model": {
        "kmeans": "run_kmeans",
        "logistic classifier": "run_log_classifier",
        "xgboost": "run_xgboost",
        "deep classifier": "run_deep_classifier",
        "automl classifier": "run_automl_classifier"
    },
    "operation": {
        "compare & select": "run_compare_and_select"
    },
    "service": {
        "deploy": "run_deploy",
        "report": "run_report"
    }
}

STRING_TO_FUNCTION_MAPPING = {
    "run_load_dataset": run_load_dataset,
    "run_train_test_split": run_train_test_split,
    "run_normalize": run_normalize,
    "run_replace_nan": run_replace_nan,
    "run_one_hot_encoding": run_one_hot_encoding,
    "run_log_transform": run_log_transform,
    "run_kmeans": run_kmeans,
    "run_log_classifier": run_log_classifier,
    "run_xgboost": run_xgboost,
    "run_deep_classifier": run_deep_classifier,
    "run_automl_classifier": run_automl_classifier,
    "run_compare_and_select": run_compare_and_select,
    "run_deploy": run_deploy,
    "run_report": run_report
}
