#!/usr/bin/env python3
"""
Módulo que define la clase GrabadorPantallaAudio, la cual graba la pantalla
con audio proveniente de 'combined.monitor'.
"""

import subprocess
import sys
import logging

logger = logging.getLogger(__name__)

class GrabadorPantallaAudio:
    """
    Clase responsable de grabar la pantalla (X11) con audio desde 'combined.monitor'.
    """

    def __init__(self, fps: int, nombre_archivo: str) -> None:
        """
        :param fps: Tasa de fotogramas (FPS).
        :param nombre_archivo: Nombre base del archivo de salida (se añadirá _pantalla.mkv).
        """
        self.fps = fps
        self.nombre_archivo = f"{nombre_archivo}_pantalla.mkv"
        self.proceso = None

    def iniciar_grabacion(self) -> None:
        """
        Inicia la grabación de la pantalla con audio desde combined.monitor,
        utilizando ffmpeg en segundo plano.
        """
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'x11grab',
            '-framerate', str(self.fps),
            '-video_size', self._obtener_resolucion_pantalla(),
            '-i', self._obtener_pantalla(),
            '-f', 'pulse',
            '-ac', '2',
            '-i', 'combined.monitor',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            self.nombre_archivo
        ]
        logger.info(f"Comando grabación pantalla: {' '.join(comando)}")
        self.proceso = subprocess.Popen(comando, stdin=subprocess.PIPE)

    def detener_grabacion(self) -> None:
        """
        Detiene la grabación enviando la tecla 'q' a ffmpeg,
        luego espera a que el proceso termine.
        """
        if self.proceso:
            logger.info("Deteniendo grabación de pantalla...")
            self.proceso.stdin.write(b'q')
            self.proceso.stdin.flush()
            self.proceso.wait()
            logger.info(f"Grabación de pantalla guardada en: {self.nombre_archivo}")

    def _obtener_resolucion_pantalla(self) -> str:
        """
        Obtiene la resolución de la pantalla usando python-xlib.
        Si no está instalado, notifica al usuario y sale del programa.
        """
        try:
            from Xlib import display
            pantalla = display.Display().screen()
            ancho = pantalla.width_in_pixels
            alto = pantalla.height_in_pixels
            return f"{ancho}x{alto}"
        except ImportError:
            logger.error("python-xlib no está instalado. Necesario para la resolución de pantalla.")
            print("Instala python-xlib: pip install python-xlib")
            sys.exit(1)

    def _obtener_pantalla(self) -> str:
        """
        Retorna la pantalla X11 en la cual se realizará la captura (por defecto ':0.0').
        Modifica si tu $DISPLAY es distinto.
        """
        return ':0.0'
