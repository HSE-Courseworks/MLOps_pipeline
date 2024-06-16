from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from io import BytesIO
import joblib
import mlflow
import pandas as pd
import os
from datetime import datetime
import sys
from reactions_predicting.cluster import clusterizer
from reactions_predicting.Tokenize import tokenizer, vectorizer
import logging
import json
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:8000", 
    "http://app:8000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], 
    allow_headers=["*"],
)



MINIO_BUCKET_NAME = "mlflow"

model=None

os.environ.update({
    "MLFLOW_TRACKING_URI": "http://mlflow:5000",
    "MLFLOW_S3_ENDPOINT_URL": "http://minio:9000",
    "AWS_ACCESS_KEY_ID": "minioadmin",
    "AWS_SECRET_ACCESS_KEY": "minioadmin"
})

minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

def load_model_from_minio(model_path):
    try:
        model_data = minio_client.get_object(MINIO_BUCKET_NAME, model_path)
        model_bytes = model_data.read()
        model = joblib.load(BytesIO(model_bytes))
        return model
    except Exception as e:
        print(f"Error loading model with joblib: {e}")
        raise HTTPException(status_code=402, detail=f"Model not found.{model_path} 1")

@app.post("/load_model/")
async def load_model(request: dict):
    model_path = request["model_path"][6+len(MINIO_BUCKET_NAME):]
    global model
    model = load_model_from_minio(model_path)

    if model is None:
        print(model_path)
        raise HTTPException(status_code=404, detail=f"Model not found.{model_path} 2")

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML model prediction API!"}

@app.post("/predict")
def predict_text(text=Body(embed=True)): 
    try:
        if not text:
            raise HTTPException(status_code=401, detail="No text provided for prediction.")
        
        global model
        try:
            if True:
                model_data = minio_client.get_object("mlflow", "37/48f742c5bc724f61baa4b49401197361/artifacts/reactions_model/reactions_model.joblib")
                model_bytes = model_data.read()
                model = joblib.load(BytesIO(model_bytes))
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Failed to load model: {str(e)}")

        try:
            experiment_name = "predict_posts"
            mlflow.set_experiment(experiment_name)
            with mlflow.start_run(run_name=f"Prediction Run - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"):
                prediction = model.predict(text)
                with open('prediction.json', 'w', encoding='utf-8') as f:
                    json.dump(prediction, f, ensure_ascii=False)
                with open("text.txt", "w") as file:
                    file.write(text)
                mlflow.log_artifact("text.txt")
                mlflow.log_artifact("prediction.json")
                return {"prediction": prediction}

        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Prediction failed: {str(e)}")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=504, detail=f"Prediction failed: {str(e)}")
