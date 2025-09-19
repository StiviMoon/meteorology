#!/usr/bin/env python3
"""
Gestor de Datos del Sistema Meteorológico
Script para gestionar la persistencia de datos
"""

import subprocess
import sys
from typing import List, Tuple

class DataManager:
    """Clase para gestionar la persistencia de datos"""

    def __init__(self):
        self.volumes = ["influxdb-data", "grafana-data"]

    def run_command(self, command: str, description: str) -> Tuple[bool, str]:
        """Ejecuta un comando del sistema"""
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {description} completado")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en {description}: {e.stderr}")
            return False, e.stderr

    def list_volumes(self) -> None:
        """Lista todos los volúmenes Docker"""
        print("📦 Volúmenes del sistema meteorológico:")
        print("-" * 45)

        success, output = self.run_command("docker volume ls", "Listando volúmenes")
        if success:
            lines = output.strip().split('\n')
            for line in lines:
                if any(vol in line for vol in self.volumes):
                    print(f"  {line}")

    def show_volume_info(self, volume_name: str) -> None:
        """Muestra información detallada de un volumen"""
        success, output = self.run_command(
            f"docker volume inspect {volume_name}",
            f"Inspeccionando volumen {volume_name}"
        )
        if success:
            print(f"\n📊 Información del volumen {volume_name}:")
            print(output)

    def backup_volumes(self) -> None:
        """Crea backup de los volúmenes"""
        print("💾 Creando backup de volúmenes...")

        for volume in self.volumes:
            success, _ = self.run_command(
                f"docker run --rm -v {volume}:/data -v $(pwd):/backup alpine tar czf /backup/{volume}-backup.tar.gz -C /data .",
                f"Backup de {volume}"
            )
            if success:
                print(f"✅ Backup creado: {volume}-backup.tar.gz")

    def restore_volumes(self) -> None:
        """Restaura volúmenes desde backup"""
        print("🔄 Restaurando volúmenes desde backup...")

        for volume in self.volumes:
            backup_file = f"{volume}-backup.tar.gz"
            success, _ = self.run_command(
                f"docker run --rm -v {volume}:/data -v $(pwd):/backup alpine tar xzf /backup/{backup_file} -C /data",
                f"Restaurando {volume}"
            )
            if success:
                print(f"✅ Volumen {volume} restaurado")

    def clean_volumes(self) -> None:
        """Limpia todos los volúmenes (ELIMINA DATOS)"""
        print("⚠️  ADVERTENCIA: Esto eliminará TODOS los datos permanentemente")
        response = input("¿Estás seguro? Escribe 'ELIMINAR' para confirmar: ")

        if response == "ELIMINAR":
            for volume in self.volumes:
                success, _ = self.run_command(
                    f"docker volume rm {volume}",
                    f"Eliminando volumen {volume}"
                )
                if success:
                    print(f"✅ Volumen {volume} eliminado")
        else:
            print("❌ Operación cancelada")

    def show_help(self) -> None:
        """Muestra ayuda del script"""
        print("🔧 Gestor de Datos del Sistema Meteorológico")
        print("=" * 50)
        print("Comandos disponibles:")
        print("  list     - Listar volúmenes")
        print("  info     - Información detallada de volúmenes")
        print("  backup   - Crear backup de datos")
        print("  restore  - Restaurar desde backup")
        print("  clean    - Eliminar todos los datos (PELIGROSO)")
        print("  help     - Mostrar esta ayuda")

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("❌ Uso: python manage_data.py <comando>")
        print("   Ejecuta 'python manage_data.py help' para ver comandos disponibles")
        sys.exit(1)

    manager = DataManager()
    command = sys.argv[1].lower()

    if command == "list":
        manager.list_volumes()
    elif command == "info":
        manager.list_volumes()
        for volume in manager.volumes:
            manager.show_volume_info(volume)
    elif command == "backup":
        manager.backup_volumes()
    elif command == "restore":
        manager.restore_volumes()
    elif command == "clean":
        manager.clean_volumes()
    elif command == "help":
        manager.show_help()
    else:
        print(f"❌ Comando desconocido: {command}")
        manager.show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
