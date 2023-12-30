#!/bin/bash

REPO_PATH="/home/sh1ron/HSE/MLOps_pipeline"

echo "Please enter the archive number (1 or 2):"
read ARCHIVE_NUM

if [ $ARCHIVE_NUM -eq 1 ]; then
    ARCHIVE_PATH="archive_1.tar"
    FILE_PATH="./dataset1/database.db"
    tar -xf $ARCHIVE_PATH
    cp $FILE_PATH $REPO_PATH
    echo "Data from archive_1 imported successfully."

elif [ $ARCHIVE_NUM -eq 2 ]; then
    ARCHIVE_PATH="archive_2.tar"
    FILE_PATH="./dataset2/database.db"
    DATA_PATH="./dataset2/data"
    tar -xf $ARCHIVE_PATH
    cp $FILE_PATH $REPO_PATH
    cp -r $DATA_PATH $REPO_PATH
    echo "Data from archive_2 imported successfully."
    
else
    echo "Invalid archive number. Please enter 1 or 2."
fi