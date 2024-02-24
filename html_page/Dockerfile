FROM python:latest
COPY . /documentation
WORKDIR /documentation
RUN pip install requests && pip install markdown && pip install bs4 && pip install html5lib
CMD ["python3", "main.py"]