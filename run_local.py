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
            "mqtt": {"url": "localhost:1883", "user": None, "pass": None}
        }

    def print_header(self) -> None:
        """Imprime el encabezado del sistema"""
        print("🌤️ " + "=" * 60)
        print(f"   {self.project_name}")
        print("=" * 62)

    def print_success(self, message: str) -> None:
        """Imprime mensaje de éxito"""
        print(f"✅ {message}")

    def print_error(self, message: str) -> None:
        """Imprime mensaje de error"""
        print(f"❌ {message}")

    def print_info(self, message: str) -> None:
        """Imprime mensaje informativo"""
        print(f"ℹ️  {message}")

    def print_warning(self, message: str) -> None:
        """Imprime mensaje de advertencia"""
        print(f"⚠️  {message}")

    def run_command(self, command: str, description: str, silent: bool = False) -> Tuple[bool, str]:
        """
        Ejecuta un comando del sistema

        Args:
            command: Comando a ejecutar
            description: Descripción del comando
            silent: Si True, no imprime mensajes de progreso

        Returns:
            Tuple[bool, str]: (éxito, salida del comando)
        """
        if not silent:
            print(f"🔄 {description}...")

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            if not silent:
                self.print_success(f"{description} completado")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            if not silent:
                self.print_error(f"Error en {description}: {e.stderr}")
            return False, e.stderr

    def check_docker(self) -> bool:
        """Verifica si Docker y Docker Compose están instalados"""
        docker_ok, _ = self.run_command("docker --version", "Verificando Docker", silent=True)
        compose_ok, _ = self.run_command("docker-compose --version", "Verificando Docker Compose", silent=True)

        if not docker_ok or not compose_ok:
            self.print_error("Docker o Docker Compose no están instalados")
            self.print_info("Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop")
            return False

        return True

    def clean_docker_system(self) -> bool:
        """Limpia el sistema Docker para evitar conflictos"""
        self.print_info("Limpiando sistema Docker...")

        # Parar todos los contenedores
        self.run_command("docker-compose down --remove-orphans", "Parando contenedores", silent=True)

        # Limpiar imágenes huérfanas
        self.run_command("docker system prune -f", "Limpiando sistema Docker", silent=True)

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

        # Verificar si las dependencias ya están instaladas
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
        # Limpiar contenedores existentes primero
        self.print_info("Limpiando contenedores existentes...")
        self.run_command("docker-compose down --remove-orphans", "Limpiando contenedores", silent=True)

        # Iniciar servicios
        success, _ = self.run_command("docker-compose up -d", "Iniciando servicios Docker")
        if success:
            self.print_info("Esperando que los servicios estén listos...")
            time.sleep(15)  # Esperar más tiempo para que los servicios estén listos

            # Verificar que los servicios estén funcionando
            self.print_info("Verificando estado de los servicios...")
            success, output = self.run_command("docker-compose ps", "Verificando servicios", silent=True)
            if success and "Up" in output:
                self.print_success("Servicios iniciados correctamente")
            else:
                self.print_warning("Algunos servicios pueden no estar funcionando correctamente")
        return success

    def check_services_status(self) -> None:
        """Verifica el estado de los servicios"""
        success, output = self.run_command("docker-compose ps", "Verificando estado de servicios", silent=True)
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
        print("   source venv/bin/activate")
        print()
        print("2. Ejecutar componentes (en terminales separadas):")
        print("   python publisher/publisher.py    # Simulador de sensores")
        print("   python subscriber/subscriber.py  # Guardar en InfluxDB")
        print()
        print("3. Comandos útiles:")
        print("   docker-compose logs -f           # Ver logs")
        print("   docker-compose down              # Parar sistema")
        print("   docker-compose ps                # Estado servicios")

    def display_data_warning(self) -> None:
        """Muestra información sobre persistencia de datos"""
        print("\n💾 Persistencia de Datos:")
        print("-" * 30)
        print("✅ Los datos se mantienen entre reinicios")
        print("✅ InfluxDB: Volumen 'influxdb-data'")
        print("✅ Grafana: Volumen 'grafana-data'")
        print()
        print("🔧 Comandos de gestión:")
        print("• docker-compose stop     # Parar sin perder datos")
        print("• docker-compose down     # Parar y eliminar contenedores")
        print("• docker-compose down -v  # Parar y ELIMINAR datos")
        print("• docker volume ls        # Ver volúmenes")
        print("• docker volume rm <name> # Eliminar volumen específico")

    def run(self) -> None:
        """Ejecuta el proceso completo de inicialización"""
        self.print_header()

        # Verificar Docker
        if not self.check_docker():
            sys.exit(1)

        # Limpiar sistema Docker si es necesario
        self.clean_docker_system()

        # Configurar entorno Python
        if not self.setup_python_environment():
            self.print_error("Error configurando entorno Python")
            sys.exit(1)

        # Iniciar servicios Docker
        if not self.start_docker_services():
            self.print_error("Error iniciando servicios Docker")
            self.print_info("Intenta ejecutar: docker-compose up -d --force-recreate")
            sys.exit(1)

        # Verificar estado
        self.check_services_status()

        # Mostrar información
        self.display_services_info()
        self.display_usage_instructions()
        self.display_data_warning()

        print("\n🎉 ¡Sistema iniciado correctamente!")
        print("=" * 62)

def main():
    """Función principal"""
    system = WeatherMonitoringSystem()
    system.run()

if __name__ == "__main__":
    main()
