from telegram_feature.telegram_utils import TelegramClient, read_tg_info
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime
import json

api_id, api_hash = read_tg_info()
session_string = "AgFfAc4ALjzMYIRz_9iLm_ptYPK5cFGQARRXPakqBwVYTf6HWie7qDJ0WD2vXLCy99QJf63OnWllsvcQreSZF5TEKY1i0tGLUM2uU8fkIYVhdrxjyKU_6F20Eh-yRiZp6nCTsPCK8GQfsOy3QqNeI0FsgPGdbcL77kZ4mPRM3Pfh2JT8NPz0CvwbLbHjRejqts8UdskIbqPqPJ-kXpnfeCBDNA7l8OaSKx11mry7VPjCXoS6iMKZt4tQAlApvN7qgSps58V-YTJe2lhtn0cIKpp_cuBktINFiFEKmF3ztOtnpTXCyWCRCdXDA9y3eQQPLsVMG657OD9KXhojzdEwv1fAD6DHrwAAAAFs60KSAA"
client = TelegramClient(api_id, api_hash, session_string)

channels = {
    "moscowach": True,
    "tinkoff_analytics_official": True
}

def retrieve_posts(client, channel_id, n, **kwargs):
    client.get_n_last_posts(channel_id, n)

def tg_channels_manager(**kwargs):
    ti = kwargs['ti']
    channels_to_retrieve = {}
    for channel_id, should_retrieve in channels.items():
        if should_retrieve:
            channels_to_retrieve[f'retrieve_posts_channel_{channel_id}'] = True
    Variable.set("channels_to_retrieve", json.dumps(channels_to_retrieve), serialize_json=True)
    return channels_to_retrieve

with DAG('tg_data_dag', description='Retrieve last n posts from Telegram channels', schedule_interval='@daily', catchup=False, default_args={
    'owner': 'bro',
    'start_date': datetime(2024, 2, 22),
    'provide_context': True
}) as dag:

    tg_channels_manager_task = BranchPythonOperator(
        task_id='tg_channels_manager',
        python_callable=tg_channels_manager,
        provide_context=True,
    )

    for channel_id, should_retrieve in channels.items():
        retrieve_posts_task = PythonOperator(
            task_id=f'retrieve_posts_channel_{channel_id}',
            python_callable=retrieve_posts,
            op_args=[client, channel_id, 150],
            provide_context=True,
        )

        tg_channels_manager_task >> retrieve_posts_task