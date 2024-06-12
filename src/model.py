import pickle
from functools import lru_cache
import time

import streamlit as st
# from sklearn.datasets import make_regression
# from sklearn.linear_model import LinearRegression


# X, y, coef = make_regression(n_samples=100, n_features=(5), n_targets=1, noise=50, coef=True)
# columns = [f"feat_{x+1}" for x in range(X.shape[1])]
# data=pd.DataFrame(X, columns=columns)

# model = LinearRegression().fit(X, y)
# score = model.score(X, y)

# Save the model to a file
# with open('./res/models/model.pkl', 'wb') as file:
#     pickle.dump(model, file)


# @st.cache_resource
@lru_cache
def load_model():
    return pickle.load(open("./res/models/model.pkl", "rb"))

def predict(data):

    model = load_model()
    return model.predict(data[:model.n_features_in_])

if __name__ == "__main__":
    import numpy as np

    start = time.perf_counter()
    result = predict(np.array([[0.0, 0.0, 0.0, 0.0, 0.0]]))
    print(f"{100 * (time.perf_counter() - start):.2f} s")
    print(result.round(2))
