from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from mlflow_experiments.main import train_and_predict_models, load_and_check_model
from mlflow_experiments.data_loader import load_iris_dataset
from mlflow_experiments.models import NaiveCustomModel
from mlflow_experiments.mlflow_logging import log_model_and_metrics
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np 
import mlflow
import os

experiment_name = "Ya sigma sigma sigma"

def setup_mlflow():
    mlflow.set_tracking_uri("http://mlflow:5000")
    os.environ['MLFLOW_TRACKING_URI'] = "http://mlflow:5000"
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://minio:9000"
    os.environ['AWS_ACCESS_KEY_ID'] = "minioadmin"
    os.environ['AWS_SECRET_ACCESS_KEY'] = "minioadmin"
    mlflow.set_experiment(experiment_name)

args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 27),
    'provide_context': True
}

def train_and_predict_models_wrapper(model_func, name, X_train, y_train, X_test, y_test, **kwargs):
    setup_mlflow()

    ti = kwargs['ti']

    name, run_id, M1, P1 = train_and_predict_models(model_func, name, X_train, y_train, X_test, y_test)

    P1_list = P1.tolist()

    ti.xcom_push(key='name', value=name)
    ti.xcom_push(key='run_id', value=run_id)
    ti.xcom_push(key='M1', value=M1)
    ti.xcom_push(key='P1', value=P1_list)

def load_and_check_model_wrapper(name, **kwargs):
    setup_mlflow()

    ti = kwargs['ti']

    name = ti.xcom_pull(key='name', task_ids=f'{name}_train_and_predict')
    run_id = ti.xcom_pull(key='run_id', task_ids=f'{name}_train_and_predict')
    M1 = ti.xcom_pull(key='M1', task_ids=f'{name}_train_and_predict')
    P1_list = ti.xcom_pull(key='P1', task_ids=f'{name}_train_and_predict')
    
    P1 = np.array(P1_list)

    load_and_check_model(run_id, name, X_test, y_test, P1, M1, experiment_name)

with DAG('mlflow_tests', description='Run models tests', schedule_interval='@daily', catchup=False, default_args=args) as dag:
    X_train, X_test, y_train, y_test = load_iris_dataset()

    for model_func, name in [
        (lambda: RandomForestRegressor(n_estimators=100, random_state=42), "RandomForest"),
        (lambda: NaiveCustomModel(), "NaiveCustomModel"),
        (lambda: LinearRegression(), "SimpleAIModel") 
    ]:

        train_and_predict_task = PythonOperator(
            task_id=f'{name}_train_and_predict',
            python_callable=train_and_predict_models_wrapper,
            op_args=[model_func, name, X_train, y_train, X_test, y_test],
            provide_context=True,
        )

        load_and_check_task = PythonOperator(
            task_id=f'{name}_load_and_check',
            python_callable=load_and_check_model_wrapper,
            op_args=[name],
            provide_context=True,
        )

        train_and_predict_task >> load_and_check_task