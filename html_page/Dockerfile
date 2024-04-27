FROM python:latest
COPY ./html_page /html_page
COPY ./documentation /documentation
RUN pip install markdown
CMD ["python3", "html_page/main.py"]