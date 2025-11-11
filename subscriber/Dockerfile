# =============================
# Etapa base
# =============================
FROM python:3.11-slim

# Configurar el entorno
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copiar dependencias
COPY subscriber.py .

# Instalar dependencias necesarias
RUN pip install --no-cache-dir paho-mqtt influxdb-client

# Crear un usuario sin privilegios (mejor práctica de seguridad)
RUN useradd -m subscriberuser
USER subscriberuser

# Comando por defecto
CMD ["python", "subscriber.py"]
