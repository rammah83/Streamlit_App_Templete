import pickle
import joblib
from functools import lru_cache
import pandas as pd

from src.helper import models, features


@lru_cache
def load_model(model_name: str = r"model01"):
    if models[model_name].endswith(".pkl"):
        return pickle.load(open(models[model_name], "rb"))
    else:
        return joblib.load(models[model_name])


def predict(data):
    model = load_model()
    return model.predict(data[: model.n_features_in_])


@lru_cache
def model_coefficients(model):
    return pd.Series(
        model.coef_, index=features.keys(), name="Coefficients"
    ).sort_values()  # type: ignore


if __name__ == "__main__":
    import numpy as np
    import time

    start = time.perf_counter()
    result = predict(
        np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "A", "AAA", "KK", "SS"]])
    )
    print(f"{100 * (time.perf_counter() - start):.2f} s")
    print(result.round(2))
