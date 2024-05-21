FROM python:3.9-slim

WORKDIR /app

COPY migration.py .

RUN pip install boto3 pymysql

CMD ["python", "migration.py"]

