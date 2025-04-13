# main.py
#
# Punto de entrada principal de la aplicación de grabación.
# Orquesta el flujo:
# 1) Verificar dependencias (pactl, ffmpeg, wmctrl opcional).
# 2) Solicitar al usuario nombre base y modo de grabación.
# 3) Configurar PulseAudio.
# 4) Iniciar la(s) grabación(es).
# 5) Esperar a que el usuario detenga.
# 6) Limpiar PulseAudio.
# 7) Finalizar.

import logging
import sys

from src.dependencies import verificar_dependencias
from src.user_input import solicitar_opciones_usuario
from src.window_manager import WindowManager
from src.pulseaudio_manager import (
    limpiar_modulos_existentes,
    crear_sink_nulo,
    configurar_loopbacks_en_combined,
    limpiar_pulseaudio
)
from src.recorders.screen_recorder import GrabadorPantallaAudio
from src.recorders.camera_recorder import GrabadorCamaraSinAudio
from src.recorders.window_recorder import GrabadorVentanaAudio


def main() -> None:
    # Configuración básica del logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    logger.info("=== Inicio de la aplicación de grabación ===")

    # 1) Verificar dependencias
    verificar_dependencias()

    # 2) Solicitar opciones de usuario (fps ya no se pregunta, viene por config)
    base_filename, modo = solicitar_opciones_usuario()

    # 3) Configurar PulseAudio
    logger.info("Limpiando módulos antiguos de PulseAudio...")
    limpiar_modulos_existentes()

    logger.info("Creando sink nulo 'combined'...")
    crear_sink_nulo()

    logger.info("Conectando fuentes al sink 'combined'...")
    configurar_loopbacks_en_combined()

    # Inicializar grabadores
    grabador_pantalla = None
    grabador_camara = None
    grabador_ventana = None

    try:
        if modo == 1:
            logger.info("Opción 1: Grabación solo de pantalla (con audio).")
            grabador_pantalla = GrabadorPantallaAudio(base_filename)
            grabador_pantalla.iniciar_grabacion()

        elif modo == 2:
            logger.info("Opción 2: Grabación de pantalla (con audio) + cámara (sin audio).")
            grabador_pantalla = GrabadorPantallaAudio(base_filename)
            grabador_camara = GrabadorCamaraSinAudio(base_filename)

            grabador_pantalla.iniciar_grabacion()
            grabador_camara.iniciar_grabacion()

        elif modo == 3:
            logger.info("Opción 3: Grabación de ventana específica (con audio).")
            ventana_id = WindowManager.seleccionar_ventana()
            if not ventana_id:
                logger.warning("No se pudo obtener el ID de la ventana. Finalizando.")
                return

            grabador_ventana = GrabadorVentanaAudio(base_filename, ventana_id)
            grabador_ventana.iniciar_grabacion()

        elif modo == 4:
            logger.info("Opción 4: Grabación de ventana específica (con audio) + cámara (sin audio).")
            ventana_id = WindowManager.seleccionar_ventana()
            if not ventana_id:
                logger.warning("No se pudo obtener el ID de la ventana. Finalizando.")
                return

            grabador_ventana = GrabadorVentanaAudio(base_filename, ventana_id)
            grabador_camara = GrabadorCamaraSinAudio(base_filename)

            grabador_ventana.iniciar_grabacion()
            grabador_camara.iniciar_grabacion()

        input("\nPresiona Enter para detener la grabación...\n")

    except KeyboardInterrupt:
        logger.warning("Grabación detenida por el usuario (Ctrl+C).")

    except Exception as e:
        logger.error(f"Ocurrió un error inesperado: {e}", exc_info=True)

    finally:
        if grabador_pantalla:
            grabador_pantalla.detener_grabacion()
        if grabador_camara:
            grabador_camara.detener_grabacion()
        if grabador_ventana:
            grabador_ventana.detener_grabacion()

        # Limpiar módulos PulseAudio
        logger.info("Limpiando módulos de PulseAudio...")
        limpiar_pulseaudio()
        logger.info("=== Fin de la aplicación de grabación ===")


if __name__ == "__main__":
    main()
