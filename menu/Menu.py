#!/usr/bin/env python3
"""
🌦️ Sistema Meteorológico - Menú Principal Integrado
Permite interactuar con los módulos:
- Publisher/Subscriber (simulación y escucha de datos)
- Análisis estadístico
- Gestión de datos (backup, restore, limpieza)
- Administración de servicios (Docker)
"""

import os
import subprocess
import sys
import time

# --- Ajuste de rutas ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Importaciones internas ---
from run_local import WeatherMonitoringSystem
from manage_data import DataManager


# --- Funciones auxiliares ---
def limpiar_pantalla():
    os.system("clear" if os.name == "posix" else "cls")

def ejecutar_script(comando, descripcion):
    """Ejecuta un script externo y muestra logs"""
    print(f"\n🔹 {descripcion}")
    print("=" * 60)
    try:
        proceso = subprocess.Popen(comando, shell=True)
        print("📡 Ejecutando... (Ctrl+C para detener si es un proceso continuo)")
        proceso.wait()
    except KeyboardInterrupt:
        print("\n⛔ Proceso detenido por el usuario.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        input("\nPresiona Enter para continuar...")


# --- Módulos ---
def iniciar_simulacion():
    ejecutar_script("python3 publisher/publisher.py", "Iniciando simulación de datos")

def iniciar_suscriptor():
    ejecutar_script("python3 subscriber/subscriber.py", "Escuchando datos MQTT")

def analisis_estadistico():
    ejecutar_script("python3 estadistica/Funciones.py", "Ejecutando módulo de análisis estadístico")

def gestion_datos(data_manager):
    limpiar_pantalla()
    print("💾 GESTIÓN DE DATOS")
    print("=" * 60)
    print("1️⃣  Listar volúmenes")
    print("2️⃣  Crear backup")
    print("3️⃣  Restaurar backup")
    print("4️⃣  Eliminar datos")
    print("5️⃣  Volver")
    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        os.system("docker volume ls")
    elif opcion == "2":
        data_manager.backup_volumes()
    elif opcion == "3":
        data_manager.restore_volumes()
    elif opcion == "4":
        data_manager.clean_volumes()
    elif opcion == "5":
        return
    else:
        print("❌ Opción no válida")
    input("Presiona Enter para continuar...")


def gestion_servicios(sistema):
    limpiar_pantalla()
    print("⚙️ GESTIÓN DE SERVICIOS DOCKER")
    print("=" * 60)
    print("1️⃣  Iniciar servicios")
    print("2️⃣  Ver estado de servicios")
    print("3️⃣  Ver información detallada")
    print("4️⃣  Volver")
    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        sistema.run()
    elif opcion == "2":
        sistema.check_services_status()
    elif opcion == "3":
        sistema.display_services_info()
    elif opcion == "4":
        return
    else:
        print("❌ Opción no válida")
    input("Presiona Enter para continuar...")


def mostrar_info_sistema(sistema):
    limpiar_pantalla()
    print("📊 INFORMACIÓN DEL SISTEMA")
    print("=" * 60)
    sistema.display_data_warning()
    input("\nPresiona Enter para continuar...")


def salir():
    print("\n👋 Cerrando el sistema...")
    time.sleep(1)
    sys.exit(0)


# --- Menú principal ---
def mostrar_menu():
    sistema = WeatherMonitoringSystem()
    data_manager = DataManager()

    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("🌦️  SISTEMA METEOROLÓGICO - MENÚ PRINCIPAL")
        print("=" * 60)
        print("""
[1] Iniciar simulación de datos (Publisher)
[2] Escuchar datos en tiempo real (Subscriber)
[3] Análisis estadístico
[4] Gestión de datos (Backup/Restore)
[5] Gestión de servicios Docker
[6] Información del sistema
[7] Salir
""")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            iniciar_simulacion()
        elif opcion == "2":
            iniciar_suscriptor()
        elif opcion == "3":
            analisis_estadistico()
        elif opcion == "4":
            gestion_datos(data_manager)
        elif opcion == "5":
            gestion_servicios(sistema)
        elif opcion == "6":
            mostrar_info_sistema(sistema)
        elif opcion == "7":
            salir()
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
            time.sleep(1)


# --- Punto de entrada ---
if __name__ == "__main__":
    mostrar_menu()
