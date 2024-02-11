import mlflow
import mlflow.sklearn
from datetime import datetime
from models import NaiveCustomModel
from sklearn.metrics import mean_squared_error

def log_model_and_metrics(model, model_name, X_train, y_train, X_test, y_test):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with mlflow.start_run(run_name=f"{model_name}_{timestamp}") as run:
        model.fit(X_train, y_train)

        if model_name == 'NaiveCustomModel':
            predictions = model.predict(model, X_test)
        else:
            predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        mlflow.log_metric("mse", mse)

        if isinstance(model, NaiveCustomModel):
            mlflow.pyfunc.log_model(model_name, python_model=model)
        else:
            mlflow.sklearn.log_model(model, f"{model_name}-model")

        return run.info.run_id

def load_and_print_model_details(run_id, name):
    artifact_path = f"mlartifacts/2/{run_id}/artifacts/{name}"

    if name == "NaiveCustomModel":
        model = mlflow.pyfunc.load_model(artifact_path)
    else:
        model = mlflow.sklearn.load_model(artifact_path + "-model")

    return model