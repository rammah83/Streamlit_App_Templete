import pandas as pd
import numpy as np
import pickle
import streamlit as st
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression


X, y, coef = make_regression(n_samples=100, n_features=(5), n_targets=1, noise=50, coef=True)
columns = [f"feat_{x+1}" for x in range(X.shape[1])]
data=pd.DataFrame(X, columns=columns)

model = LinearRegression().fit(X, y)
score = model.score(X, y)

# Save the model to a file
# with open('./res/models/model.pkl', 'wb') as file:
#     pickle.dump(model, file)

st.cache_resource
def load_model():
    return pickle.load(open('./res/models/model.pkl', "rb"))

if __name__ == "__main__":
    result = model.predict(np.array([[0.0, .0, .0, .0, .0]]))
    print(result)