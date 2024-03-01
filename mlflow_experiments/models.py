import numpy as np
from mlflow.pyfunc import PythonModel

class NaiveCustomModel(PythonModel):
    def fit(self, X, y):
        return self

    def predict(self, context, model_input):
        return np.ones(len(model_input))