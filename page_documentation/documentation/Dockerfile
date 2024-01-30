FROM python:latest
COPY . /documentation
WORKDIR /documentation
RUN pip install requests && pip install markdown
CMD ["python3", "main.py"]