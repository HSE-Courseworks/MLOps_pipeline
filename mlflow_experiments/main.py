import mlflow
import numpy as np
import os
from mlflow_experiments.data_loader import load_iris_dataset
from mlflow_experiments.models import NaiveCustomModel
from mlflow_experiments.mlflow_logging import log_model_and_metrics, load_and_print_model_details, predict_model
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

def fit_and_predict_model(model, X_train, y_train, X_test):
    model.fit(X_train, y_train)
    predictions = predict_model(model, X_test)
    return predictions

def train_and_predict_models(model_func, name, X_train, y_train, X_test, y_test):
    model = model_func()
    run_id = log_model_and_metrics(model, name, X_train, y_train, X_test, y_test)
    P1 = predict_model(model, X_test)
    M1 = round(mean_squared_error(y_test, P1), 4)
    return name, run_id, M1, P1

def load_and_check_model(run_id, name, X_test, y_test, P1, M1, experiment_name):
    model_2 = load_and_print_model_details(run_id, name, experiment_name)
    P2 = model_2.predict(X_test)
    M2 = round(mean_squared_error(y_test, P2), 4)
    predictions_equal = np.allclose(P1, P2)
    metrics_close = abs(M1 - M2) <= 0.001
    print(f"Model: {name}, Predictions Equal: {predictions_equal}, Metrics Close: {metrics_close}")

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("CI/CD tests")
    
    X_train, X_test, y_train, y_test = load_iris_dataset()
    
    model_functions = [
        (lambda: RandomForestRegressor(n_estimators=100, random_state=42), "RandomForest"),
        (lambda: NaiveCustomModel(), "NaiveCustomModel"),
        (lambda: LinearRegression(), "SimpleAIModel")
    ]
    
    for model_func, name in model_functions:
        name, run_id, M1, P1 = train_and_predict_models(model_func, name, X_train, y_train, X_test, y_test)
        load_and_check_model(run_id, name, X_test, y_test, P1, M1)   