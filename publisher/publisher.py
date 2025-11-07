#!/usr/bin/env python3
import time
import random
import json
import os
import paho.mqtt.client as mqtt

# =============================
# CONFIGURACIÓN
# =============================

# Permite cambiar el broker sin tocar el código (desde variable de entorno)
BROKER = os.getenv("MQTT_BROKER", "localhost")  # Usa "mosquitto" si estás dentro de Docker
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "weather/station1")

# =============================
# CLIENTE MQTT
# =============================

client = mqtt.Client()
print(f"🔌 Connecting to {BROKER}:{PORT}")

# Intentar conexión al broker
while True:
    try:
        client.connect(BROKER, PORT, 60)
        print("✅ Connected successfully to MQTT broker!")
        break
    except Exception as e:
        print(f"⚠️  Connection failed: {e}. Retrying in 5 seconds...")
        time.sleep(5)

# =============================
# LOOP DE PUBLICACIÓN
# =============================

print("📡 Starting weather data simulation...\nPress Ctrl+C to stop.\n")

try:
    while True:
        # Generación de datos simulados
        payload = {
            "temperature": round(random.uniform(20, 30), 2),
            "humidity": round(random.uniform(40, 70), 2),
            "pressure": round(random.uniform(950, 1050), 2),
            "timestamp": int(time.time()),
        }

        # Envío al broker
        client.publish(TOPIC, json.dumps(payload))
        print(f"📤 Sent: {payload}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 Publicación detenida por el usuario.")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
finally:
    client.disconnect()
    print("🔒 Disconnected from broker.")
