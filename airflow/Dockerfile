FROM apache/airflow:2.7.2
COPY ./telegram_feature ./dags/telegram_feature
USER root
RUN touch ./dags/telegram_feature/database.db
RUN chown -R "$(id -u)" ./dags/telegram_feature
USER airflow
RUN pip3 install -U pyrogram