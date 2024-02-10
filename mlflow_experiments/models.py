import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

class NaiveCustomModel(BaseEstimator, RegressorMixin):
    def __init__(self):
        pass

    def fit(self, X, y):
        return self

    def predict(self, X):
        return np.ones(X.shape[0])

def naive_custom_model():
    return NaiveCustomModel()

def simple_ai_model():
    return LinearRegression()

def random_forest_model():
    return RandomForestRegressor(n_estimators=100)