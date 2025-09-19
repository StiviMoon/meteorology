FROM python:3.11-slim
WORKDIR /app
COPY subscriber.py .
RUN pip install paho-mqtt influxdb-client
CMD ["python", "subscriber.py"]
