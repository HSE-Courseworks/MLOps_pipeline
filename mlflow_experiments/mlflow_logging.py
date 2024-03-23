import mlflow
from mlflow.sklearn import log_model
from datetime import datetime
from mlflow_experiments.models import NaiveCustomModel
from sklearn.metrics import mean_squared_error


def predict_model(model, X_test):
    if isinstance(model, NaiveCustomModel):
        return model.predict(model, X_test)
    else:
        return model.predict(X_test)


def log_model_and_metrics(model, model_name, X_train, y_train, X_test, y_test):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    model_type = "naive" if isinstance(model, NaiveCustomModel) else "sklearn"
    with mlflow.start_run(run_name=f"{model_name}_{timestamp}") as run:
        model.fit(X_train, y_train)
        predictions = predict_model(model, X_test)
        mse = mean_squared_error(y_test, predictions)
        mlflow.log_metric("mse", mse)
        if model_type == "sklearn":
            mlflow.sklearn.log_model(model, f"{model_name}-model")
        else:
            mlflow.pyfunc.log_model(model_name, python_model=model)
        return run.info.run_id


def load_and_print_model_details(run_id, name, experiment_name):
    print(experiment_name)
    artifact_path = f"s3://mlflow/{mlflow.get_experiment_by_name(experiment_name).experiment_id}/{run_id}/artifacts/{name}"
    model_type = "naive" if name == "NaiveCustomModel" else "sklearn"
    if model_type == "sklearn":
        return mlflow.sklearn.load_model(artifact_path + "-model")
    else:
        return mlflow.pyfunc.load_model(artifact_path)
