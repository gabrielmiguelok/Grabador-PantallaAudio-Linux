# dependencies.py
#
# Módulo para verificar dependencias necesarias:
# - pactl
# - ffmpeg
# - wmctrl (opcional)

import shutil
import sys
import logging

logger = logging.getLogger(__name__)

def verificar_dependencias() -> None:
    # Verifica 'pactl' y 'ffmpeg'. Si no están, se sale del programa.
    # 'wmctrl' es opcional, solo si se quiere grabar ventanas específicas.
    if not shutil.which('pactl'):
        logger.error("Error: 'pactl' no está instalado o no está en el PATH.")
        print("Instala 'pulseaudio-utils' o 'pipewire-pulse' según tu distro.")
        sys.exit(1)

    if not shutil.which('ffmpeg'):
        logger.error("Error: 'ffmpeg' no está instalado o no está en el PATH.")
        print("Instala 'ffmpeg' con el gestor de paquetes de tu distro.")
        sys.exit(1)

    if not shutil.which('wmctrl'):
        logger.warning("Advertencia: 'wmctrl' no está instalado. "
                       "No podrás listar ventanas gráficamente.")
        print("Para grabar ventanas específicas, instala 'wmctrl'.")

    logger.info("Dependencias verificadas correctamente.")
