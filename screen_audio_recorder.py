#!/usr/bin/env python3
import subprocess
import sys
import shutil

def verificar_dependencias():
    """
    Verifica que pactl y ffmpeg estén instalados en el sistema.
    """
    if not shutil.which('pactl'):
        print("Error: 'pactl' no está instalado o no se encuentra en el PATH.")
        print("Instala 'pulseaudio-utils' o pipewire-pulse según tu distro.")
        sys.exit(1)

    if not shutil.which('ffmpeg'):
        print("Error: 'ffmpeg' no está instalado o no se encuentra en el PATH.")
        print("Instala 'ffmpeg' con el gestor de paquetes de tu distro.")
        sys.exit(1)

def obtener_entrada_usuario():
    """
    Solicita al usuario los FPS y el nombre de archivo de salida.
    """
    fps_input = input("Ingresa la tasa de fotogramas (FPS, predeterminado 30): ")
    fps = int(fps_input) if fps_input else 30

    nombre_archivo_input = input("Nombre de archivo de salida (sin extensión, predeterminado 'grabacion'): ")
    nombre_archivo = nombre_archivo_input if nombre_archivo_input else "grabacion"

    return fps, nombre_archivo

def limpiar_modulos_existentes():
    """
    Descarga (unload) todos los módulos null-sink y loopback
    para empezar desde cero.
    """
    subprocess.run(['pactl', 'unload-module', 'module-null-sink'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(['pactl', 'unload-module', 'module-loopback'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def crear_sink_nulo():
    """
    Crea un sink nulo llamado 'combined'.
    Luego lo desmutea y lo pone al 100% de volumen.
    """
    subprocess.run([
        'pactl', 'load-module', 'module-null-sink',
        'sink_name=combined',
        'sink_properties=device.description=CombinedSink'
    ], check=True)

    # Subimos volumen al 100% y desmuteamos el sink "combined".
    subprocess.run(['pactl', 'set-sink-mute', 'combined', '0'], check=True)
    subprocess.run(['pactl', 'set-sink-volume', 'combined', '100%'], check=True)

def obtener_sinks():
    """
    Devuelve una lista con los nombres de todos los sinks disponibles
    (columna 2 de 'pactl list short sinks').
    """
    cmd = ['pactl', 'list', 'short', 'sinks']
    resultado = subprocess.run(cmd, capture_output=True, text=True, check=True)
    sinks = []
    for linea in resultado.stdout.strip().split('\n'):
        if not linea:
            continue
        partes = linea.split('\t')
        if len(partes) > 1:
            sinks.append(partes[1])
    return sinks

def obtener_sources():
    """
    Devuelve una lista con los nombres de todas las sources disponibles
    (columna 2 de 'pactl list short sources').
    """
    cmd = ['pactl', 'list', 'short', 'sources']
    resultado = subprocess.run(cmd, capture_output=True, text=True, check=True)
    sources = []
    for linea in resultado.stdout.strip().split('\n'):
        if not linea:
            continue
        partes = linea.split('\t')
        if len(partes) > 1:
            sources.append(partes[1])
    return sources

def configurar_loopbacks_en_combined():
    """
    - Para cada sink => conectamos su monitor al null sink 'combined',
      EXCEPTO si se trata del propio 'combined.monitor' (para evitar bucle).
    - Para cada source REAL (que no sea .monitor) => también se conecta a 'combined'.

    Adicionalmente, subimos el volumen de micrófonos a ~100% o 150% si hace falta.
    """
    sinks = obtener_sinks()
    sources = obtener_sources()

    # 1) Conectar todos los monitores de cada sink (excepto combined.monitor)
    for sink in sinks:
        monitor_name = sink + '.monitor'
        # Evitar loopback recursivo si se trata de combined
        if "combined" in sink:
            # No enlazamos combined.monitor => combined
            continue

        subprocess.run([
            'pactl', 'load-module', 'module-loopback',
            f'sink=combined',
            f'source={monitor_name}'
        ], check=True)

    # 2) Conectar todas las sources REALES (descartar .monitor)
    for source in sources:
        if '.monitor' not in source:
            # Sube el volumen de la fuente a 100% (opcionalmente 150% si es muy bajo).
            subprocess.run(['pactl', 'set-source-mute', source, '0'], check=True)
            subprocess.run(['pactl', 'set-source-volume', source, '100%'], check=True)

            subprocess.run([
                'pactl', 'load-module', 'module-loopback',
                f'sink=combined',
                f'source={source}'
            ], check=True)

def limpiar_pulseaudio():
    """
    Limpia (unload) los módulos de PulseAudio después de la grabación,
    para no dejar loopbacks permanentes.
    """
    try:
        subprocess.run(['pactl', 'unload-module', 'module-null-sink'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['pactl', 'unload-module', 'module-loopback'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error al limpiar PulseAudio: {e}")

class GrabadorPantallaAudio:
    """
    Clase para grabar la pantalla y el audio mezclado en 'combined.monitor'.
    """
    def __init__(self, fps, nombre_archivo):
        self.fps = fps
        self.nombre_archivo = f"{nombre_archivo}.mkv"
        self.proceso = None

    def iniciar_grabacion(self):
        """
        Usa ffmpeg para:
          - Capturar pantalla con x11grab
          - Capturar audio desde 'combined.monitor' con Pulse
          - Codificar con libx264 + AAC
        """
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'x11grab',
            '-framerate', str(self.fps),
            '-video_size', self.obtener_resolucion_pantalla(),
            '-i', self.obtener_pantalla(),
            '-f', 'pulse',
            '-ac', '2',
            '-i', 'combined.monitor',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            self.nombre_archivo
        ]

        self.proceso = subprocess.Popen(comando, stdin=subprocess.PIPE)

    def detener_grabacion(self):
        """
        Envía 'q' a ffmpeg para detener la grabación limpiamente.
        """
        if self.proceso:
            self.proceso.stdin.write(b'q')
            self.proceso.stdin.flush()
            self.proceso.wait()
            print(f"Grabación guardada en {self.nombre_archivo}")

    def obtener_resolucion_pantalla(self):
        """
        Detecta la resolución de la pantalla usando python-xlib.
        Si no está instalado, pide instalarlo y sale.
        """
        try:
            from Xlib import display
            pantalla = display.Display().screen()
            ancho = pantalla.width_in_pixels
            alto = pantalla.height_in_pixels
            return f"{ancho}x{alto}"
        except ImportError:
            print("Se requiere el módulo python-xlib (pip install python-xlib) para capturar la pantalla en Linux.")
            sys.exit(1)

    def obtener_pantalla(self):
        """
        Devuelve ':0.0' como pantalla a capturar por defecto.
        Cambia si tu DISPLAY es distinto.
        """
        return ':0.0'

def main():
    verificar_dependencias()
    try:
        fps, nombre_archivo = obtener_entrada_usuario()

        print("Limpiando módulos viejos (null-sink, loopback)...")
        limpiar_modulos_existentes()

        print("Creando sink nulo 'combined' y desmuteándolo...")
        crear_sink_nulo()

        print("Conectando TODAS las fuentes y monitores (excepto 'combined.monitor') al 'combined'...")
        configurar_loopbacks_en_combined()

        grabador = GrabadorPantallaAudio(fps, nombre_archivo)
        print("\nIniciando grabación de pantalla + TODO el audio (micrófonos y monitores).")
        grabador.iniciar_grabacion()

        input("\nPresiona Enter para detener la grabación...")
        grabador.detener_grabacion()

    except KeyboardInterrupt:
        print("\nGrabación detenida por el usuario (Ctrl+C).")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar un comando externo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("\nLimpiando módulos PulseAudio (null-sink y loopback)...")
        limpiar_pulseaudio()
        print("Proceso finalizado.")

if __name__ == "__main__":
    main()
