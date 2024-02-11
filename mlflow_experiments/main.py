import mlflow
import numpy as np
from data_loader import load_iris_dataset
from models import naive_custom_model, simple_ai_model, random_forest_model
from mlflow_logging import log_model_and_metrics, load_and_print_model_details
from sklearn.metrics import mean_squared_error
from prettytable import PrettyTable

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("CI/CD tests")

X_train, X_test, y_train, y_test = load_iris_dataset()

model_functions = [
    (lambda: random_forest_model(seed=42), "RandomForest"),
    (naive_custom_model, "NaiveCustomModel"),
    (simple_ai_model, "SimpleAIModel")
]

table = PrettyTable(['Model Name', 'Run ID', 'Mean Squared Error', 'Equal Predictions', 'Equal Metrics'])

for model_func, name in model_functions:
    model_1 = model_func()
    model_1.fit(X_train, y_train)

    if name == 'NaiveCustomModel':
        P1 = model_1.predict(model_1, X_test)
    else:
        P1 = model_1.predict(X_test)
    M1 = round(mean_squared_error(y_test, P1),   4)
    
    run_id = log_model_and_metrics(model_1, name, X_train, y_train, X_test, y_test)
    
    # ==============================================================================

    model_2 = load_and_print_model_details(run_id, name)
    
    P2 = model_2.predict(X_test)
    M2 = round(mean_squared_error(y_test, P2),  4)

    predictions_equal = np.allclose(P1, P2)
    metrics_close = abs(M1 - M2) <=  0.001
    
    table.add_row([name, run_id, M1, predictions_equal, metrics_close])

print(table)