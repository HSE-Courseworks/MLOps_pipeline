if [ ! -f /usr/local/bin/mc ]; then 
    sudo curl -o /usr/local/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc; 
    sudo chmod +x /usr/local/bin/mc
fi
mc alias set myminio http://localhost:9000 user minio_password
mc ls myminio/mlops 2>/dev/null || mc mb myminio/mlops