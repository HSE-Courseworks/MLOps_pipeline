FROM python:latest
COPY . /html_page
WORKDIR /html_page
RUN pip install requests && pip install markdown && pip install bs4 && pip install html5lib
CMD ["python3", "main.py"]