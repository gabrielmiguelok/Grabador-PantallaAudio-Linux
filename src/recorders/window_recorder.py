#!/usr/bin/env python3
"""
Módulo que define la clase GrabadorVentanaAudio, para grabar una ventana específica
(con audio desde 'combined.monitor').
"""

import subprocess
import logging

logger = logging.getLogger(__name__)

class GrabadorVentanaAudio:
    """
    Clase para grabar una ventana específica en X11, con audio desde 'combined.monitor'.
    """

    def __init__(self, fps: int, nombre_archivo: str, ventana_id: str) -> None:
        """
        :param fps: Tasa de fotogramas (FPS).
        :param nombre_archivo: Nombre base del archivo de salida (se añadirá _ventana.mkv).
        :param ventana_id: ID de la ventana en formato hexadecimal (p. ej. '0x03800007').
        """
        self.fps = fps
        self.ventana_id = ventana_id
        self.output_file = f"{nombre_archivo}_ventana.mkv"
        self.process = None

    def iniciar_grabacion(self) -> None:
        """
        Inicia la grabación de la ventana específica (identificada por ventana_id),
        con audio proveniente de combined.monitor, usando ffmpeg.
        """
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'x11grab',
            '-framerate', str(self.fps),
            '-window_id', self.ventana_id,
            '-i', ':0.0',  # Ajustar si tu DISPLAY es distinto
            '-f', 'pulse',
            '-ac', '2',
            '-i', 'combined.monitor',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            self.output_file
        ]
        logger.info(f"Comando grabación ventana: {' '.join(comando)}")
        self.process = subprocess.Popen(comando, stdin=subprocess.PIPE)

    def detener_grabacion(self) -> None:
        """
        Detiene la grabación enviando la tecla 'q' a ffmpeg,
        luego espera a que el proceso termine.
        """
        if self.process:
            logger.info("Deteniendo grabación de ventana...")
            self.process.stdin.write(b'q')
            self.process.stdin.flush()
            self.process.wait()
            logger.info(f"Grabación de ventana guardada en: {self.output_file}")
