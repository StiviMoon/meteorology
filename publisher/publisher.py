import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "mosquitto"
PORT = 1883
TOPIC = "weather/station1"

client = mqtt.Client()
print(f"Connecting to {BROKER}:{PORT}")
try:
    client.connect(BROKER, PORT, 60)
    print("Connected successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

while True:
    payload = {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "pressure": round(random.uniform(950, 1050), 2),
        "timestamp": int(time.time()),
    }
    client.publish(TOPIC, json.dumps(payload))
    print("Sent:", payload)
    time.sleep(5)
