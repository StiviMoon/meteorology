import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions

# MQTT config
BROKER = "mosquitto"
PORT = 1883
TOPIC = "weather/station1"

# InfluxDB config
INFLUX_URL = "http://influxdb:8086"
INFLUX_TOKEN = "admin:admin123"
ORG = "weather-org"
BUCKET = "weather-bucket"

client_influx = InfluxDBClient(url=INFLUX_URL, username="admin", password="admin123", org=ORG)
write_api = client_influx.write_api(write_options=WriteOptions(batch_size=1))

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    point = (
        Point("weather")
        .tag("station", "station1")
        .field("temperature", payload["temperature"])
        .field("humidity", payload["humidity"])
        .field("pressure", payload["pressure"])
        .time(payload["timestamp"], write_precision="s")
    )
    write_api.write(bucket=BUCKET, record=point)
    print("Saved to Influx:", payload)

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
print(f"Connecting to {BROKER}:{PORT}")
try:
    mqtt_client.connect(BROKER, PORT, 60)
    print("Connected successfully!")
    mqtt_client.subscribe(TOPIC)
    print(f"Subscribed to {TOPIC}")
    mqtt_client.loop_forever()
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)
