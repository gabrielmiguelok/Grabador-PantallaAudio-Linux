# pulseaudio_manager.py
#
# Módulo para la gestión de PulseAudio:
# - descargar módulos antiguos
# - crear sink nulo
# - configurar loopbacks
# - limpiar al finalizar

import subprocess
import logging
from src import config

logger = logging.getLogger(__name__)

def limpiar_modulos_existentes() -> None:
    # Descarga (unload) todos los módulos null-sink y loopback
    try:
        subprocess.run(['pactl', 'unload-module', 'module-null-sink'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['pactl', 'unload-module', 'module-loopback'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al limpiar módulos existentes: {e}")

def crear_sink_nulo() -> None:
    # Crea un sink nulo llamado 'combined', lo desmutea y lo pone al volumen configurado.
    try:
        subprocess.run([
            'pactl', 'load-module', 'module-null-sink',
            'sink_name=combined',
            'sink_properties=device.description=CombinedSink'
        ], check=True)

        subprocess.run(['pactl', 'set-sink-mute', 'combined', '0'], check=True)
        subprocess.run(['pactl', 'set-sink-volume', 'combined', config.DEFAULT_VOLUME], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al crear sink nulo: {e}")
        raise

def configurar_loopbacks_en_combined() -> None:
    # Conecta los monitores de todos los sinks (excepto 'combined.monitor')
    # y las fuentes reales al sink 'combined'.
    sinks = _obtener_sinks()
    sources = _obtener_sources()

    for sink in sinks:
        if "combined" in sink:
            continue
        monitor_name = f"{sink}.monitor"
        try:
            subprocess.run([
                'pactl', 'load-module', 'module-loopback',
                f'sink=combined',
                f'source={monitor_name}'
            ], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al conectar monitor {monitor_name} -> combined: {e}")

    for source in sources:
        if '.monitor' in source:
            continue
        try:
            subprocess.run(['pactl', 'set-source-mute', source, '0'], check=True)
            subprocess.run(['pactl', 'set-source-volume', source, config.DEFAULT_VOLUME], check=True)
            subprocess.run([
                'pactl', 'load-module', 'module-loopback',
                f'sink=combined',
                f'source={source}'
            ], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al conectar source {source} -> combined: {e}")

def limpiar_pulseaudio() -> None:
    # Descarga todos los módulos 'module-null-sink' y 'module-loopback'.
    try:
        subprocess.run(['pactl', 'unload-module', 'module-null-sink'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['pactl', 'unload-module', 'module-loopback'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al limpiar PulseAudio: {e}")

def _obtener_sinks() -> list[str]:
    try:
        resultado = subprocess.run(
            ['pactl', 'list', 'short', 'sinks'],
            capture_output=True, text=True, check=True
        )
        sinks = []
        for linea in resultado.stdout.strip().split('\n'):
            if not linea:
                continue
            partes = linea.split('\t')
            if len(partes) > 1:
                sinks.append(partes[1])
        return sinks
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al obtener sinks: {e}")
        return []

def _obtener_sources() -> list[str]:
    try:
        resultado = subprocess.run(
            ['pactl', 'list', 'short', 'sources'],
            capture_output=True, text=True, check=True
        )
        sources = []
        for linea in resultado.stdout.strip().split('\n'):
            if not linea:
                continue
            partes = linea.split('\t')
            if len(partes) > 1:
                sources.append(partes[1])
        return sources
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al obtener sources: {e}")
        return []
