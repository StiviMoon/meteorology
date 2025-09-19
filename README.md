# Weather Monitoring System

Sistema de monitoreo meteorológico con MQTT, InfluxDB y Grafana.

## 🚀 Inicio rápido

### Opción 1: Script automático
```bash
python3 run_local.py
```

### Opción 2: Manual
```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar servicios Docker
docker-compose up -d

# 4. Ejecutar localmente (opcional)
python publisher/publisher.py
python subscriber/subscriber.py
```

## 📊 Servicios

- **Grafana**: http://localhost:3000 (admin/admin123)
- **InfluxDB**: <http://localhost:8086> (admin/admin123)
- **URL TOKEN** http://influxdb:8086
- **TOKEN** Generado desde influx
- **MQTT Broker**: localhost:1883

### Ejemplo de peticion para temperatura
```
from(bucket: "weather-bucket")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "weather")
  |> filter(fn: (r) => r["_field"] == "temperature")
  |> filter(fn: (r) => r["station"] == "station1")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

## 🛠️ Desarrollo

### Estructura del proyecto
```
Meteorologia/
├── venv/                    # Entorno virtual Python
├── publisher/               # Simulador de datos
├── subscriber/              # Consumidor de datos
├── mosquitto/              # Configuración MQTT
├── requirements.txt        # Dependencias Python
├── docker-compose.yml      # Servicios Docker
└── run_local.py           # Script de inicio
```

### Comandos útiles
```bash
# Ver logs
docker-compose logs -f

# Parar sistema
docker-compose down

# Reconstruir contenedores
docker-compose up --build -d
```

## 🔧 Configuración

- **Publisher**: Envía datos cada 5 segundos
- **Subscriber**: Guarda datos en InfluxDB
- **Datos simulados**: Temperatura (20-30°C), Humedad (40-70%), Presión (950-1050 mbar)
