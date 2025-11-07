#!/usr/bin/env python3
import json
import time
import os
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions

# =============================
# CONFIGURACIÓN
# =============================

BROKER = os.getenv("MQTT_BROKER", "localhost")  # Usa "mosquitto" si estás dentro de Docker
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "weather/station1")

INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "admin:admin123")
ORG = os.getenv("INFLUX_ORG", "weather-org")
BUCKET = os.getenv("INFLUX_BUCKET", "weather-bucket")

# =============================
# CONEXIÓN A INFLUXDB
# =============================

print(f"🔗 Connecting to InfluxDB at {INFLUX_URL}...")
try:
    client_influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    write_api = client_influx.write_api(write_options=WriteOptions(batch_size=1))
    print("✅ Connected to InfluxDB successfully!")
except Exception as e:
    print(f"❌ Failed to connect to InfluxDB: {e}")
    exit(1)

# =============================
# CALLBACK DEL SUSCRIPTOR
# =============================

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"📩 Received: {payload}")

        # Crear punto para InfluxDB
        point = (
            Point("weather")
            .tag("station", "station1")
            .field("temperature", payload["temperature"])
            .field("humidity", payload["humidity"])
            .field("pressure", payload["pressure"])
            .time(payload["timestamp"], write_precision="s")
        )

        write_api.write(bucket=BUCKET, record=point)
        print("✅ Data written to InfluxDB successfully!\n")

    except Exception as e:
        print(f"⚠️ Error processing message: {e}")
        print("Mensaje recibido:", msg.payload.decode())

# =============================
# CLIENTE MQTT
# =============================

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

print(f"🔌 Connecting to MQTT broker {BROKER}:{PORT}")
while True:
    try:
        mqtt_client.connect(BROKER, PORT, 60)
        print("✅ Connected to MQTT broker!")
        mqtt_client.subscribe(TOPIC)
        print(f"📡 Subscribed to topic: {TOPIC}\n")
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"⚠️ Connection failed: {e}. Retrying in 5 seconds...")
        time.sleep(5)
