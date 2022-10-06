FROM python:3.10

WORKDIR /main

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]