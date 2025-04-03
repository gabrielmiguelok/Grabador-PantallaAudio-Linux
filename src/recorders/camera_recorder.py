#!/usr/bin/env python3
"""
Módulo que define la clase GrabadorCamaraSinAudio, la cual graba desde /dev/video0
o la cámara seleccionada, sin capturar audio.
"""

import subprocess
import logging

logger = logging.getLogger(__name__)

class GrabadorCamaraSinAudio:
    """
    Clase responsable de grabar la cámara sin audio (por defecto /dev/video0),
    a una resolución de 640x480 y usando la tasa de fotogramas indicada.
    """

    def __init__(self, fps: int, nombre_archivo: str) -> None:
        """
        :param fps: Tasa de fotogramas (FPS).
        :param nombre_archivo: Nombre base del archivo de salida (se añadirá _camara.mkv).
        """
        self.fps = fps
        self.nombre_archivo = f"{nombre_archivo}_camara.mkv"
        self.proceso = None

    def iniciar_grabacion(self) -> None:
        """
        Inicia la grabación de la cámara usando ffmpeg en segundo plano,
        sin capturar audio.
        """
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'v4l2',
            '-framerate', str(self.fps),
            '-video_size', '640x480',
            '-i', '/dev/video0',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-pix_fmt', 'yuv420p',
            self.nombre_archivo
        ]
        logger.info(f"Comando grabación cámara: {' '.join(comando)}")
        self.proceso = subprocess.Popen(comando, stdin=subprocess.PIPE)

    def detener_grabacion(self) -> None:
        """
        Detiene la grabación enviando la tecla 'q' a ffmpeg,
        luego espera a que el proceso termine.
        """
        if self.proceso:
            logger.info("Deteniendo grabación de cámara...")
            self.proceso.stdin.write(b'q')
            self.proceso.stdin.flush()
            self.proceso.wait()
            logger.info(f"Grabación de cámara (SIN audio) guardada en: {self.nombre_archivo}")
