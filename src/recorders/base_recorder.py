# base_recorder.py
#
# Clase base para otros grabadores. Contiene:
# - Manejo de FPS desde config.
# - Generación de ruta de salida única (si existe, agrega x2, x3, ...).
# - Subdirectorio dinámico según fecha (definido en config).

import os
import logging
from src import config

logger = logging.getLogger(__name__)

class BaseRecorder:
    def __init__(self):
        # Se establece el FPS desde la configuración global
        self.fps = config.DEFAULT_FPS
        self.process = None
        self.output_file = None

    def generar_ruta_salida_unica(self, base_filename: str, suffix: str) -> str:
        # Genera una ruta de salida dentro de la carpeta con fecha,
        # añade "_suffix" y si el archivo existe, le agrega x2, x3, etc.

        final_dir = config.get_recording_directory_path()
        tentative_name = f"{base_filename}_{suffix}.mkv"
        full_path = os.path.join(final_dir, tentative_name)

        if not os.path.exists(full_path):
            return full_path

        # Si ya existe, iterar x2, x3, x4...
        count = 2
        while True:
            alt_name = f"{base_filename}_{suffix}x{count}.mkv"
            alt_path = os.path.join(final_dir, alt_name)
            if not os.path.exists(alt_path):
                return alt_path
            count += 1

    def iniciar_grabacion(self):
        # Debe implementarse en clases hijas
        raise NotImplementedError

    def detener_grabacion(self):
        # Detiene la grabación enviando 'q' a ffmpeg
        if self.process:
            logger.info(f"Deteniendo grabación en {self.output_file}")
            self.process.stdin.write(b'q')
            self.process.stdin.flush()
            self.process.wait()
            logger.info(f"Grabación finalizada y guardada en: {self.output_file}")
