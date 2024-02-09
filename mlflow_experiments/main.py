import mlflow
from data_loader import load_iris_dataset
from models import naive_custom_model, simple_ai_model, random_forest_model
from mlflow_logging import log_model_and_metrics

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("CI/CD tests")

X_train, X_test, y_train, y_test = load_iris_dataset()

log_model_and_metrics(random_forest_model(), "RandomForest", X_train, y_train, X_test, y_test)
log_model_and_metrics(naive_custom_model(), "NaiveCustomModel", X_train, y_train, X_test, y_test)
log_model_and_metrics(simple_ai_model(), "SimpleAIModel", X_train, y_train, X_test, y_test)