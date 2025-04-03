#!/usr/bin/env python3
"""
Módulo para la gestión de PulseAudio: creación de sink nulo, loopbacks, limpieza, etc.

Contiene funciones que ayudan a:
- Descargar módulos antiguos (sink nulo, loopback).
- Crear y configurar un sink nulo.
- Conectar monitores de los sinks y fuentes reales al nuevo sink.
- Limpiar al finalizar.
"""

import subprocess
import logging

logger = logging.getLogger(__name__)

def limpiar_modulos_existentes() -> None:
    """
    Descarga (unload) todos los módulos null-sink y loopback
    para iniciar un entorno PulseAudio limpio.
    """
    try:
        subprocess.run(['pactl', 'unload-module', 'module-null-sink'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['pactl', 'unload-module', 'module-loopback'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al limpiar módulos existentes: {e}")

def crear_sink_nulo() -> None:
    """
    Crea un sink nulo llamado 'combined', lo desmutea y lo configura al 100% de volumen.
    Este sink se utilizará para combinar las fuentes de audio de distintos orígenes.
    """
    try:
        subprocess.run([
            'pactl', 'load-module', 'module-null-sink',
            'sink_name=combined',
            'sink_properties=device.description=CombinedSink'
        ], check=True)

        subprocess.run(['pactl', 'set-sink-mute', 'combined', '0'], check=True)
        subprocess.run(['pactl', 'set-sink-volume', 'combined', '100%'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al crear sink nulo: {e}")
        raise

def configurar_loopbacks_en_combined() -> None:
    """
    Conecta los monitores de todos los sinks (excepto el nuevo combined.monitor)
    y las fuentes reales al sink 'combined', creando los loopbacks necesarios.

    De esta manera, cualquier audio que se reproduzca o capture por otros sinks
    se enviará también al nuevo sink combinado.
    """
    sinks = _obtener_sinks()
    sources = _obtener_sources()

    # Conectar monitores de cada sink
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

    # Conectar fuentes reales (no monitores)
    for source in sources:
        if '.monitor' in source:
            continue
        try:
            subprocess.run(['pactl', 'set-source-mute', source, '0'], check=True)
            subprocess.run(['pactl', 'set-source-volume', source, '100%'], check=True)
            subprocess.run([
                'pactl', 'load-module', 'module-loopback',
                f'sink=combined',
                f'source={source}'
            ], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al conectar source {source} -> combined: {e}")

def limpiar_pulseaudio() -> None:
    """
    Deshace (unload) todos los módulos 'module-null-sink' y 'module-loopback' de PulseAudio,
    dejando el sistema en un estado similar al inicial (antes de ejecutar la aplicación).
    """
    try:
        subprocess.run(['pactl', 'unload-module', 'module-null-sink'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['pactl', 'unload-module', 'module-loopback'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al limpiar PulseAudio: {e}")

def _obtener_sinks() -> list[str]:
    """
    Obtiene la lista de nombres de sinks disponibles en PulseAudio.
    Por ejemplo: ['alsa_output.pci-0000_00_1b.0.analog-stereo', 'combined']
    """
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
    """
    Obtiene la lista de nombres de sources disponibles en PulseAudio.
    Por ejemplo: ['alsa_output.pci-0000_00_1b.0.analog-stereo.monitor', 'alsa_input.usb-...']
    """
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
