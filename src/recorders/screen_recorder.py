# screen_recorder.py
#
# Clase para grabar la pantalla con audio desde combined.monitor.

import subprocess
import sys
import logging
from src.recorders.base_recorder import BaseRecorder
from src import config

logger = logging.getLogger(__name__)

class GrabadorPantallaAudio(BaseRecorder):
    def __init__(self, base_filename: str):
        super().__init__()
        self.output_file = self.generar_ruta_salida_unica(base_filename, "pantalla")

    def iniciar_grabacion(self):
        # Inicia la grabación de la pantalla en segundo plano con ffmpeg
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'x11grab',
            '-framerate', str(self.fps),
            '-video_size', self._obtener_resolucion_pantalla(),
            '-i', config.DEFAULT_DISPLAY,
            '-f', 'pulse',
            '-ac', '2',
            '-i', 'combined.monitor',
            '-c:v', config.VIDEO_CODEC,
            '-preset', config.FFMPEG_PRESET,
            '-c:a', config.AUDIO_CODEC,
            '-pix_fmt', 'yuv420p',
            self.output_file
        ]

        logger.info(f"Comando grabación pantalla: {' '.join(comando)}")
        self.process = subprocess.Popen(comando, stdin=subprocess.PIPE)

    def _obtener_resolucion_pantalla(self) -> str:
        # Obtiene la resolución de la pantalla con python-xlib, si está instalado.
        try:
            from Xlib import display
            pantalla = display.Display().screen()
            ancho = pantalla.width_in_pixels
            alto = pantalla.height_in_pixels
            return f"{ancho}x{alto}"
        except ImportError:
            logger.error("python-xlib no está instalado. Necesario para resolución de pantalla.")
            print("Instala python-xlib: pip install python-xlib")
            sys.exit(1)
