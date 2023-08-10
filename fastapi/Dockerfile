FROM python:3.10

WORKDIR /fastapi

COPY ./fastapi/ ./

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]