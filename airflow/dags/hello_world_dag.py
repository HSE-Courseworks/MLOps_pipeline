from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

args = {
    'owner': 'dimon',
    'start_date':datetime(2018, 11, 1),
    'provide_context':True
}

def hello_world(**kwargs):
    ti = kwargs['ti']
    print("Hello world!")

with DAG('Hello-world', description='Hello-world', schedule_interval='*/6 * * * *',  catchup=False, default_args=args) as dag:
    t1 = PythonOperator(task_id='task_1', python_callable=hello_world)
    t1
