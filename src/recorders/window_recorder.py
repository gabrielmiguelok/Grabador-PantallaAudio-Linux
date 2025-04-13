# window_recorder.py
#
# Clase para grabar una ventana específica (con audio desde combined.monitor).

import subprocess
import logging
from src.recorders.base_recorder import BaseRecorder
from src import config

logger = logging.getLogger(__name__)

class GrabadorVentanaAudio(BaseRecorder):
    def __init__(self, base_filename: str, ventana_id: str):
        super().__init__()
        self.ventana_id = ventana_id
        self.output_file = self.generar_ruta_salida_unica(base_filename, "ventana")

    def iniciar_grabacion(self):
        # Inicia la grabación de una ventana específica
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'x11grab',
            '-framerate', str(self.fps),
            '-window_id', self.ventana_id,
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

        logger.info(f"Comando grabación ventana: {' '.join(comando)}")
        self.process = subprocess.Popen(comando, stdin=subprocess.PIPE)
