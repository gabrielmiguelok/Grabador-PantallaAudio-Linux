# camera_recorder.py
#
# Clase para grabar la cámara sin audio.

import subprocess
import logging
from src.recorders.base_recorder import BaseRecorder
from src import config

logger = logging.getLogger(__name__)

class GrabadorCamaraSinAudio(BaseRecorder):
    def __init__(self, base_filename: str):
        super().__init__()
        self.output_file = self.generar_ruta_salida_unica(base_filename, "camara")

    def iniciar_grabacion(self):
        # Inicia la grabación de la cámara usando ffmpeg,
        # sin capturar audio.
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'v4l2',
            '-framerate', str(self.fps),
            '-video_size', config.CAMERA_RESOLUTION,
            '-i', config.CAMERA_DEVICE,
            '-c:v', config.VIDEO_CODEC,
            '-preset', config.FFMPEG_PRESET,
            '-pix_fmt', 'yuv420p',
            self.output_file
        ]

        logger.info(f"Comando grabación cámara: {' '.join(comando)}")
        self.process = subprocess.Popen(comando, stdin=subprocess.PIPE)
