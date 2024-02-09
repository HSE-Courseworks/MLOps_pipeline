import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

class NaiveCustomModel(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.mean_ = None

    def fit(self, X, y):
        self.mean_ = np.mean(y)
        return self

    def predict(self, X):
        return np.full(X.shape[0], self.mean_)

def naive_custom_model():
    return NaiveCustomModel()

def simple_ai_model():
    model = LinearRegression()
    return model

def random_forest_model():
    model = RandomForestRegressor(n_estimators=100)
    return model