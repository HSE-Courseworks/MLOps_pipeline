mc alias set myminio http://minio:9000 user minio_password
mc ls myminio/mlops 2>/dev/null || mc mb myminio/mlops