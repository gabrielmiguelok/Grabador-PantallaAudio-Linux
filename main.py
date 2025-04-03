#!/usr/bin/env python3
# =============================================================================
# MIT License
#
# Copyright (c) 2025 Gabriel Hércules Miguel
#
# Por la presente se concede permiso, libre de cargos, a cualquier persona que
# obtenga una copia de este software y de los archivos de documentación
# asociados (el "Software"), a utilizar el Software sin restricción, incluyendo
# sin limitación los derechos a usar, copiar, modificar, fusionar, publicar,
# distribuir, sublicenciar y/o vender copias del Software, y a permitir a las
# personas a las que se les proporcione el Software a hacer lo mismo, sujeto a
# las siguientes condiciones:
#
# El aviso de copyright anterior y este aviso de permiso se incluirán en todas
# las copias o partes sustanciales del Software.
#
# EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA
# O IMPLÍCITA, INCLUIDAS, ENTRE OTRAS, LAS GARANTÍAS DE COMERCIALIZACIÓN,
# IDONEIDAD PARA UN FIN DETERMINADO Y NO INFRACCIÓN. EN NINGÚN CASO LOS
# AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN,
# DAÑO U OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN CONTRACTUAL, AGRAVIO O DE
# CUALQUIER OTRA MANERA, QUE SURJA DE, FUERA DE O EN CONEXIÓN CON EL SOFTWARE
# O EL USO U OTROS TRATOS EN EL SOFTWARE.
# =============================================================================
"""
Punto de entrada principal de la aplicación de grabación de pantalla/ventana/cámara.

Este script coordina:
1) Verificar dependencias necesarias.
2) Solicitar al usuario FPS, nombre base de archivo y modo de grabación.
3) Configurar PulseAudio (creando un sink nulo y loopbacks).
4) Iniciar la(s) grabación(es) según el modo seleccionado.
5) Esperar hasta que el usuario decida detener la grabación.
6) Limpiar módulos de PulseAudio y terminar.
"""

import logging
import sys

# Módulos locales
from src.dependencies import verificar_dependencias
from src.user_input import solicitar_opciones_usuario
from src.window_manager import seleccionar_ventana
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
    """
    Función principal de la aplicación. Orquesta el flujo general de grabación.
    """
    # Configuración básica del registro (logging)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    logger.info("=== Inicio de la aplicación de grabación ===")

    # 1) Verificar dependencias (pactl, ffmpeg, wmctrl opcional)
    verificar_dependencias()

    # 2) Solicitar opciones de usuario
    fps, base_filename, modo = solicitar_opciones_usuario()

    # 3) Configurar PulseAudio
    logger.info("Limpiando módulos antiguos de PulseAudio...")
    limpiar_modulos_existentes()

    logger.info("Creando sink nulo 'combined'...")
    crear_sink_nulo()

    logger.info("Conectando fuentes al sink 'combined'...")
    configurar_loopbacks_en_combined()

    # Inicializar grabadores (posibles)
    grabador_pantalla = None
    grabador_camara = None
    grabador_ventana = None

    try:
        if modo == 1:
            logger.info("Opción 1: Grabación solo de pantalla (con audio).")
            grabador_pantalla = GrabadorPantallaAudio(fps, base_filename)
            grabador_pantalla.iniciar_grabacion()

        elif modo == 2:
            logger.info("Opción 2: Grabación de pantalla (con audio) + cámara (sin audio).")
            grabador_pantalla = GrabadorPantallaAudio(fps, base_filename)
            grabador_camara = GrabadorCamaraSinAudio(fps, base_filename)

            grabador_pantalla.iniciar_grabacion()
            grabador_camara.iniciar_grabacion()

        elif modo == 3:
            logger.info("Opción 3: Grabación de ventana específica (con audio).")
            ventana_id = seleccionar_ventana()
            if not ventana_id:
                logger.warning("No se pudo obtener el ID de la ventana. Finalizando.")
                return

            grabador_ventana = GrabadorVentanaAudio(fps, base_filename, ventana_id)
            grabador_ventana.iniciar_grabacion()

        elif modo == 4:
            logger.info("Opción 4: Grabación de ventana específica (con audio) + cámara (sin audio).")
            ventana_id = seleccionar_ventana()
            if not ventana_id:
                logger.warning("No se pudo obtener el ID de la ventana. Finalizando.")
                return

            grabador_ventana = GrabadorVentanaAudio(fps, base_filename, ventana_id)
            grabador_camara = GrabadorCamaraSinAudio(fps, base_filename)

            grabador_ventana.iniciar_grabacion()
            grabador_camara.iniciar_grabacion()

        input("\nPresiona Enter para detener la grabación...\n")

    except KeyboardInterrupt:
        logger.warning("Grabación detenida por el usuario (Ctrl+C).")

    except Exception as e:
        logger.error(f"Ocurrió un error inesperado: {e}", exc_info=True)

    finally:
        # Detener grabaciones si se iniciaron
        if grabador_pantalla:
            grabador_pantalla.detener_grabacion()
        if grabador_camara:
            grabador_camara.detener_grabacion()
        if grabador_ventana:
            grabador_ventana.detener_grabacion()

        # Limpiar módulos de PulseAudio
        logger.info("Limpiando módulos de PulseAudio...")
        limpiar_pulseaudio()
        logger.info("=== Fin de la aplicación de grabación ===")


if __name__ == "__main__":
    main()
