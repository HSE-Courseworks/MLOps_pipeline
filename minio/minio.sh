mc alias set myminio http://minio:9000 minioadmin minioadmin
mc ls myminio/mlflow 2>/dev/null || mc mb myminio/mlflow