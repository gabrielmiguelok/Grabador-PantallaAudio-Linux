# window_manager.py
#
# Módulo para gestionar y listar ventanas abiertas en el sistema usando 'wmctrl'.
# Proporciona funciones para:
# - Verificar si 'wmctrl' está disponible.
# - Listar ventanas abiertas (id, título).
# - Permitir al usuario seleccionar una ventana.

import subprocess
import logging
import shutil

logger = logging.getLogger(__name__)

class WindowManager:
    # Clase para gestionar la detección y selección de ventanas vía wmctrl.

    @staticmethod
    def listar_ventanas() -> list[dict]:
        # Retorna una lista de ventanas en formato:
        # [
        #   {
        #     'id': '0x04a00003',
        #     'titulo': 'Mi ventana'
        #   },
        #   ...
        # ]
        if not WindowManager._existe_wmctrl():
            return []

        try:
            output = subprocess.check_output(['wmctrl', '-l'], text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al ejecutar wmctrl: {e}")
            return []

        ventanas = []
        for linea in output.splitlines():
            partes = linea.split(None, 3)
            if len(partes) < 4:
                continue
            ventana_id = partes[0]
            titulo = partes[3]
            ventanas.append({'id': ventana_id, 'titulo': titulo})
        return ventanas

    @staticmethod
    def seleccionar_ventana() -> str:
        # Muestra la lista de ventanas y solicita elección al usuario.
        ventanas = WindowManager.listar_ventanas()
        if not ventanas:
            print("No se encontraron ventanas (o 'wmctrl' no está disponible).")
            logger.warning("No se encontraron ventanas o no se pudo usar 'wmctrl'.")
            return None

        print("\nVentanas detectadas:")
        for i, ventana in enumerate(ventanas, start=1):
            print(f"{i}. {ventana['titulo']} (ID: {ventana['id']})")

        while True:
            eleccion = input("Elige una ventana por número: ").strip()
            if eleccion.isdigit():
                idx = int(eleccion) - 1
                if 0 <= idx < len(ventanas):
                    return ventanas[idx]['id']
            print("Selección inválida, intenta nuevamente.")

    @staticmethod
    def _existe_wmctrl() -> bool:
        # Verifica si el binario 'wmctrl' se encuentra en el PATH.
        return bool(shutil.which('wmctrl'))
