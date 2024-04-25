FROM python:3.8
WORKDIR /fastapi
RUN pip install "fastapi[all]" pytest
COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--reload","--host", "0.0.0.0" ]