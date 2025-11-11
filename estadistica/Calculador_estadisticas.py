import time
from datetime import datetime
import sys
import os
from typing import Union, Any, List
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# ==========================================================
# MÓDULOS PERSONALIZADOS
# ==========================================================
from Funciones import (
    calcular_mediana,
    calcular_moda,
    calcular_std_dev,
    calcular_iqr
)

# ==========================================================
# LIBRERÍAS DE InfluxDB
# ==========================================================
try:
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
except ImportError:
    print("❌ ERROR: Instala el paquete 'influxdb-client' con: pip install influxdb-client")
    sys.exit(1)

# ==========================================================
# CONFIGURACIÓN GLOBAL
# ==========================================================
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "weather-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "weather-bucket")

STATION_ID = "station1"
CAMPO_A_ANALIZAR = "temperature"
PERIODO_ANALISIS = "2h"
INTERVALO_REPETICION = 60  # segundos

# Validación de token
if not INFLUX_TOKEN:
    print("❌ ERROR: No se encontró el INFLUX_TOKEN. Configúralo en el archivo .env")
    sys.exit(1)

# ==========================================================
# FUNCIONES PRINCIPALES
# ==========================================================

def obtener_datos_influx(client: InfluxDBClient) -> List[Union[float, int]]:
    """Consulta InfluxDB y devuelve una lista de valores numéricos válidos."""
    query_api = client.query_api()
    consulta_flux = f"""
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{PERIODO_ANALISIS})
      |> filter(fn: (r) => r["_measurement"] == "weather")
      |> filter(fn: (r) => r["_field"] == "{CAMPO_A_ANALIZAR}")
      |> filter(fn: (r) => r["station"] == "{STATION_ID}")
      |> keep(columns: ["_value"])
    """

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📡 Consultando {CAMPO_A_ANALIZAR} (últimas {PERIODO_ANALISIS})...")

    try:
        tables = query_api.query(query=consulta_flux, org=INFLUX_ORG)
        valores = [
            record.get_value()
            for table in tables for record in table.records
            if isinstance(record.get_value(), (int, float))
        ]
        print(f"✅ {len(valores)} puntos válidos obtenidos.")
        return valores
    except Exception as e:
        print(f"⚠️ Error al consultar InfluxDB: {e}")
        return []


def escribir_estadisticas(client: InfluxDBClient, estadisticas: dict):
    """Guarda las estadísticas calculadas en una nueva measurement."""
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = (
        Point("estadisticas_clima")
        .tag("station", STATION_ID)
        .tag("campo", CAMPO_A_ANALIZAR)
        .field("mediana", estadisticas["mediana"])
        .field("std_dev", estadisticas["std_dev"])
        .field("iqr", estadisticas["iqr"])
        .time(datetime.utcnow())
    )

    # Manejo flexible de la moda
    if estadisticas["moda"] is not None:
        if isinstance(estadisticas["moda"], list):
            point.field("moda", float(estadisticas["moda"][0]))
        else:
            point.field("moda", float(estadisticas["moda"]))

    try:
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(
            f"📝 Guardado: Mediana={estadisticas['mediana']:.2f} | "
            f"Moda={estadisticas['moda']} | "
            f"StdDev={estadisticas['std_dev']:.2f} | IQR={estadisticas['iqr']:.2f}"
        )
    except Exception as e:
        print(f"⚠️ Error al escribir estadísticas en InfluxDB: {e}")


def procesar_datos(datos: List[Union[float, int]]) -> dict:
    """Calcula las estadísticas básicas sobre los datos recibidos."""
    if not datos:
        return {}

    return {
        "mediana": calcular_mediana(datos),
        "moda": calcular_moda(datos),
        "std_dev": calcular_std_dev(datos),
        "iqr": calcular_iqr(datos),
    }


# ==========================================================
# BUCLE PRINCIPAL
# ==========================================================

def main():
    print(f"🔗 Conectando a InfluxDB ({INFLUX_URL}) ...")
    try:
        client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
        client.ping()
        print("✅ Conexión establecida correctamente.")
    except Exception as e:
        print(f"❌ No se pudo conectar a InfluxDB: {e}")
        sys.exit(1)

    with client:
        while True:
            print("============================================================")
            datos = obtener_datos_influx(client)
            
            if not datos:
                print("⚠️ No hay datos disponibles, esperando siguiente ciclo...")
            else:
                stats = procesar_datos(datos)
                if all(stats.values()):
                    escribir_estadisticas(client, stats)
                else:
                    print("⚠️ No se pudieron calcular todas las estadísticas (datos insuficientes).")
            
            print(f"⏳ Esperando {INTERVALO_REPETICION} segundos para la siguiente iteración...\n")
            time.sleep(INTERVALO_REPETICION)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido manualmente. Cerrando conexión...")
        sys.exit(0)
