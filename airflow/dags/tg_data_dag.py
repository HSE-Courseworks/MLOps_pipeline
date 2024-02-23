import sys
sys.path.insert(1, '/home/sh1ron/HSE/MLOps_pipeline/telegram_feature')

from telegram_utils import TelegramClient, read_tg_channels
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

args = {
    'owner': 'bro',
    'start_date': datetime(2024,  2,  22),
    'provide_context': True
}

dag = DAG(
    'tg_data_dag',
    description='Retrieve last n posts from Telegram channels',
    schedule_interval='*/2 * * * *',
    catchup=False,
    default_args=args
)

def retrieve_posts(channel_id, n, **kwargs):
    api_id, api_hash = read_tg_info()
    client = TelegramClient(api_id, api_hash)
    client.get_n_last_posts(channel_id, n)

channels = read_tg_channels()
for i, channel_id in enumerate(channels):
    task = PythonOperator(
        task_id=f'retrieve_posts_channel_{i}',
        python_callable=retrieve_posts,
        op_args=[channel_id,  150],   
        dag=dag
    )