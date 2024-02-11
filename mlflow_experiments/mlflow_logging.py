import mlflow
import mlflow.sklearn
from datetime import datetime
from sklearn.metrics import mean_squared_error

def log_model_and_metrics(model, model_name, X_train, y_train, X_test, y_test):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with mlflow.start_run(run_name=f"{model_name}_{timestamp}") as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(model, f"{model_name}-model")