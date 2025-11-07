#!/usr/bin/env python3
"""
Sistema de Monitoreo Meteorológico
Script de gestión para el sistema completo de monitoreo meteorológico
"""

import subprocess
import os
import sys
import time
from typing import Tuple

class WeatherMonitoringSystem:
    """Clase principal para gestionar el sistema de monitoreo meteorológico"""

    def __init__(self):
        self.project_name = "Sistema de Monitoreo Meteorológico"
        self.services = {
            "grafana": {"url": "http://localhost:3000", "user": "admin", "pass": "admin123"},
            "influxdb": {"url": "http://localhost:8086", "user": "admin", "pass": "admin123"},
            "mqtt": {"url": "http://localhost:1883", "user": None, "pass": None}
        }
        # aquí guardaremos el comando correcto de docker compose
        self.compose_cmd = None

    def print_header(self) -> None:
        """Imprime el encabezado del sistema"""
        print("🌤️ " + "=" * 60)
        print(f"   {self.project_name}")
        print("=" * 62)

    def print_success(self, message: str) -> None:
        print(f"✅ {message}")

    def print_error(self, message: str) -> None:
        print(f"❌ {message}")

    def print_info(self, message: str) -> None:
        print(f"ℹ️  {message}")

    def print_warning(self, message: str) -> None:
        print(f"⚠️  {message}")

    def run_command(self, command, description: str, silent: bool = False) -> Tuple[bool, str]:
        """
        Ejecuta un comando del sistema.
        'command' puede ser string o lista.
        """
        if isinstance(command, list):
            shell_flag = False
        else:
            shell_flag = True

        if not silent:
            print(f"🔄 {description}...")

        try:
            result = subprocess.run(
                command,
                shell=shell_flag,
                check=True,
                capture_output=True,
                text=True
            )
            if not silent:
                self.print_success(f"{description} completado")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            if not silent:
                self.print_error(f"Error en {description}: {e.stderr.strip()}")
            return False, e.stderr

    def check_docker(self) -> bool:
        """Verifica si Docker y Docker Compose (v1 o v2) están instalados"""
        # comprobar docker engine
        docker_ok, _ = self.run_command(["docker", "--version"], "Verificando Docker", silent=True)
        if not docker_ok:
            self.print_error("Docker no está instalado")
            self.print_info("Instala Docker desde: https://docs.docker.com/engine/install/")
            return False

        # probar docker compose v2
        success, _ = self.run_command(["docker", "compose", "version"], "Verificando Docker Compose v2", silent=True)
        if success:
            self.compose_cmd = ["docker", "compose"]
            return True

        # probar docker-compose v1
        success, _ = self.run_command(["docker-compose", "--version"], "Verificando Docker Compose v1", silent=True)
        if success:
            self.compose_cmd = ["docker-compose"]
            return True

        # ninguna versión encontrada
        self.print_error("Docker Compose no está instalado (ni v1 ni v2)")
        self.print_info("Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop")
        return False

    def clean_docker_system(self) -> bool:
        """Limpia el sistema Docker para evitar conflictos"""
        self.print_info("Limpiando sistema Docker...")
        # Parar todos los contenedores
        self.run_command(self.compose_cmd + ["down", "--remove-orphans"], "Parando contenedores", silent=True)
        # Limpiar imágenes huérfanas
        self.run_command(["docker", "system", "prune", "-f"], "Limpiando sistema Docker", silent=True)
        return True

    def setup_python_environment(self) -> bool:
        """Configura el entorno virtual de Python"""
        if not os.path.exists("venv"):
            self.print_info("Entorno virtual no encontrado, creando uno nuevo...")
            success, _ = self.run_command("python3 -m venv venv", "Creando entorno virtual")
            if not success:
                return False
        else:
            self.print_info("Entorno virtual encontrado, verificando dependencias...")

        success, _ = self.run_command(
            "venv/bin/pip list | grep -E '(paho-mqtt|influxdb-client)'",
            "Verificando dependencias existentes",
            silent=True
        )
        if not success:
            self.print_info("Instalando dependencias Python...")
            success, _ = self.run_command(
                "venv/bin/pip install -r requirements.txt",
                "Instalando dependencias Python"
            )
        else:
            self.print_success("Dependencias ya instaladas")
        return success

    def start_docker_services(self) -> bool:
        """Inicia los servicios Docker"""
        self.print_info("Limpiando contenedores existentes...")
        self.run_command(self.compose_cmd + ["down", "--remove-orphans"], "Limpiando contenedores", silent=True)

        success, _ = self.run_command(self.compose_cmd + ["up", "-d"], "Iniciando servicios Docker")
        if success:
            self.print_info("Esperando que los servicios estén listos...")
            time.sleep(15)

            self.print_info("Verificando estado de los servicios...")
            success, output = self.run_command(self.compose_cmd + ["ps"], "Verificando servicios", silent=True)
            if success and "Up" in output:
                self.print_success("Servicios iniciados correctamente")
            else:
                self.print_warning("Algunos servicios pueden no estar funcionando correctamente")
        return success

    def check_services_status(self) -> None:
        """Verifica el estado de los servicios"""
        success, output = self.run_command(self.compose_cmd + ["ps"], "Verificando estado de servicios", silent=True)
        if success:
            print("\n📊 Estado de los servicios:")
            print(output)

    def display_services_info(self) -> None:
        """Muestra información de los servicios disponibles"""
        print("\n🌐 Servicios disponibles:")
        print("-" * 40)
        for service, config in self.services.items():
            print(f"• {service.upper()}:")
            print(f"  URL: {config['url']}")
            if config['user']:
                print(f"  Usuario: {config['user']}")
                print(f"  Contraseña: {config['pass']}")
            print()

    def display_usage_instructions(self) -> None:
        """Muestra instrucciones de uso"""
        print("🔧 Instrucciones de uso:")
        print("-" * 30)
        print("1. Activar entorno virtual:")
        print("   source venv/bin/activate\n")
        print("2. Ejecutar componentes (en terminales separadas):")
        print("   python publisher/publisher.py    # Simulador de sensores")
        print("   python subscriber/subscriber.py  # Guardar en InfluxDB\n")
        print("3. Comandos útiles:")
        print(f"   {' '.join(self.compose_cmd)} logs -f           # Ver logs")
        print(f"   {' '.join(self.compose_cmd)} down              # Parar sistema")
        print(f"   {' '.join(self.compose_cmd)} ps                # Estado servicios")

    def display_data_warning(self) -> None:
        """Muestra información sobre persistencia de datos"""
        print("\n💾 Persistencia de Datos:")
        print("-" * 30)
        print("✅ Los datos se mantienen entre reinicios")
        print("✅ InfluxDB: Volumen 'influxdb-data'")
        print("✅ Grafana: Volumen 'grafana-data'\n")
        print("🔧 Comandos de gestión:")
        print(f"• {' '.join(self.compose_cmd)} stop     # Parar sin perder datos")
        print(f"• {' '.join(self.compose_cmd)} down     # Parar y eliminar contenedores")
        print(f"• {' '.join(self.compose_cmd)} down -v  # Parar y ELIMINAR datos")
        print("• docker volume ls        # Ver volúmenes")
        print("• docker volume rm <name> # Eliminar volumen específico")

    def run(self) -> None:
        """Ejecuta el proceso completo de inicialización"""
        self.print_header()
        if not self.check_docker():
            sys.exit(1)
        self.clean_docker_system()
        if not self.setup_python_environment():
            self.print_error("Error configurando entorno Python")
            sys.exit(1)
        if not self.start_docker_services():
            self.print_error("Error iniciando servicios Docker")
            self.print_info(f"Intenta ejecutar: {' '.join(self.compose_cmd)} up -d --force-recreate")
            sys.exit(1)
        self.check_services_status()
        self.display_services_info()
        self.display_usage_instructions()
        self.display_data_warning()
        print("\n🎉 ¡Sistema iniciado correctamente!")
        print("=" * 62)

def main():
    system = WeatherMonitoringSystem()
    system.run()

if __name__ == "__main__":
    main()
