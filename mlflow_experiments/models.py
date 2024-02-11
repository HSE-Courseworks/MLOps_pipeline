import numpy as np
from mlflow.pyfunc import PythonModel
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

class NaiveCustomModel(PythonModel):
    def fit(self, X, y):
        return self

    def predict(self, context, model_input):
        return np.ones(len(model_input))
  
def naive_custom_model():
    return NaiveCustomModel()

def simple_ai_model():
    return LinearRegression()

def random_forest_model(seed=None):
    return RandomForestRegressor(n_estimators=100, random_state=seed)