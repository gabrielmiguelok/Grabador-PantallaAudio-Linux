#!/usr/bin/env python3
"""
Módulo para verificar dependencias necesarias para la aplicación.

Verifica:
- 'pactl' (para manipular PulseAudio o PipeWire).
- 'ffmpeg' (para grabar con video y audio).
- 'wmctrl' (opcional, para listar ventanas).
"""

import shutil
import sys
import logging

logger = logging.getLogger(__name__)

def verificar_dependencias() -> None:
    """
    Verifica que 'pactl' y 'ffmpeg' estén instalados.
    Si no lo están, finaliza la ejecución.
    También recomienda instalar 'wmctrl' si se desea grabar ventanas específicas.
    """
    # pactl
    if not shutil.which('pactl'):
        logger.error("Error: 'pactl' no está instalado o no se encuentra en el PATH.")
        print("Instala 'pulseaudio-utils' o 'pipewire-pulse' según tu distro.")
        sys.exit(1)

    # ffmpeg
    if not shutil.which('ffmpeg'):
        logger.error("Error: 'ffmpeg' no está instalado o no se encuentra en el PATH.")
        print("Instala 'ffmpeg' con el gestor de paquetes de tu distro.")
        sys.exit(1)

    # wmctrl (opcional)
    if not shutil.which('wmctrl'):
        logger.warning("Advertencia: 'wmctrl' no está instalado. "
                       "No podrás listar ventanas correctamente.")
        print("Advertencia: Para grabar ventanas específicas, instala 'wmctrl'.")

    logger.info("Dependencias verificadas correctamente.")
