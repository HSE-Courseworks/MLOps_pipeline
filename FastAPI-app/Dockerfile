FROM python:3.8
RUN pip install "fastapi[all]" pytest joblib minio mlflow pymorphy2 emoji gensim faiss-cpu dill boto3
COPY ./FastAPI-app ./FastAPI-app
COPY ./reactions_predicting ./reactions_predicting
CMD ["uvicorn", "FastAPI-app.app.main:app", "--reload","--host", "0.0.0.0" ]