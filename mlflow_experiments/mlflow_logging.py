import mlflow
from mlflow.sklearn import log_model
from datetime import datetime
from models import NaiveCustomModel
from sklearn.metrics import mean_squared_error

def log_sklearn_model(model, model_name, X_train, y_train, X_test, y_test, timestamp):
    with mlflow.start_run(run_name=f"{model_name}_{timestamp}") as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(model, f"{model_name}-model")
        return run.info.run_id

def log_naive_model(model, model_name, X_train, y_train, X_test, y_test, timestamp):
    with mlflow.start_run(run_name=f"{model_name}_{timestamp}") as run:
        model.fit(X_train, y_train)
        predictions = model.predict(model, X_test)
        mse = mean_squared_error(y_test, predictions)
        mlflow.log_metric("mse", mse)
        mlflow.pyfunc.log_model(model_name, python_model=model)
        return run.info.run_id

def log_model_and_metrics(model, model_name, X_train, y_train, X_test, y_test):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if isinstance(model, NaiveCustomModel):
        return log_naive_model(model, model_name, X_train, y_train, X_test, y_test, timestamp)
    return log_sklearn_model(model, model_name, X_train, y_train, X_test, y_test, timestamp)

def load_sklearn_model(artifact_path):
    return mlflow.sklearn.load_model(artifact_path + "-model")

def load_naive_model(artifact_path):
    return mlflow.pyfunc.load_model(artifact_path)

def load_and_print_model_details(run_id, name):
    artifact_path = f"mlartifacts/2/{run_id}/artifacts/{name}"
    if name == "NaiveCustomModel":
        return load_naive_model(artifact_path)
    return load_sklearn_model(artifact_path)