# Grabador Pantalla, Ventanas y Cámara con Audio en Linux

[![Licencia MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Índice

1. [Descripción](#descripción)
2. [Características](#características)
3. [Requisitos](#requisitos)
4. [Instalación](#instalación)
    - [Dependencias de Python](#dependencias-de-python)
    - [Dependencias del Sistema](#dependencias-del-sistema)
5. [Uso](#uso)
6. [Contribuciones](#contribuciones)
7. [Contacto](#contacto)

---

## Descripción

Esta aplicación permite **grabar la pantalla completa, una ventana específica o tu cámara web en Linux**, capturando y combinando simultáneamente **todas las fuentes de audio** del sistema (micrófonos, aplicaciones, música, etc.) en un único archivo multimedia, utilizando **ffmpeg** y **PulseAudio**.

El proyecto se encarga automáticamente de configurar un sink de audio combinado, simplificando considerablemente el proceso de captura de audio y vídeo.

> **Repositorio oficial**: [Grabador-PantallaAudio-Linux](https://github.com/gabrielmiguelok/Grabador-PantallaAudio-Linux)
> Autor: Gabriel Hércules Miguel (Licencia MIT)

---

## Características

- ✅ **Grabación versátil**:
  - Pantalla completa con audio.
  - Pantalla completa con audio y cámara web sin audio.
  - Ventana específica con audio.
  - Ventana específica con audio más cámara web sin audio.

- ✅ **Configuración automática de PulseAudio**:
  - Creación de un **sink nulo** ("combined") que mezcla todas las fuentes.
  - Loopbacks automáticos desde fuentes de audio hacia el sink combinado.

- ✅ **Sencillez y facilidad de uso**:
  - Interfaz interactiva simple (CLI).
  - Configuración rápida (FPS, nombre de archivo y modo de grabación).

- ✅ **Limpieza automática**:
  - Se restauran automáticamente las configuraciones originales de PulseAudio al finalizar la grabación.

- ✅ **Optimizado para Linux**:
  - Usa `pactl` para PulseAudio o PipeWire con soporte de PulseAudio.
  - Usa `ffmpeg` para codificación (video en h264, audio AAC).

---

## Requisitos

### Dependencias de Python

- **Python 3.7+**
- **python-xlib**

### Dependencias del Sistema

- **ffmpeg**
- **pulseaudio-utils** (o **pipewire-pulse** compatible con pactl)
- **wmctrl** (opcional pero recomendado para grabar ventanas específicas)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/gabrielmiguelok/Grabador-PantallaAudio-Linux.git
cd Grabador-PantallaAudio-Linux
```

### 2. Crear y activar entorno virtual (opcional)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 4. Instalar dependencias del sistema

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install ffmpeg pulseaudio-utils wmctrl
```

**Arch/Manjaro:**

```bash
sudo pacman -S ffmpeg pipewire-pulse wmctrl
```

**Otras distribuciones:**

Utiliza el gestor de paquetes de tu distribución para instalar `ffmpeg`, `pulseaudio-utils` o `pipewire-pulse`, y `wmctrl`.

---

## Uso

### Ejecutar el script

```bash
python main.py
```

### Seleccionar opciones

- **FPS** (por defecto 30): Introduce la tasa de fotogramas deseada.
- **Nombre del archivo** (por defecto `grabacion`): Introduce un nombre base para los archivos generados.
- **Modo de grabación**:
  - **1**: Pantalla completa con audio.
  - **2**: Pantalla completa con audio + cámara (sin audio).
  - **3**: Ventana específica con audio.
  - **4**: Ventana específica con audio + cámara (sin audio).

### Iniciar y detener grabación

- Para detener la grabación, presiona **Enter** o usa `Ctrl+C`.
- Los archivos resultantes se guardan en la carpeta del proyecto:
  - Ejemplo:
    - `grabacion_pantalla.mkv`
    - `grabacion_camara.mkv`
    - `grabacion_ventana.mkv`

---

## Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz un **fork** del repositorio.
2. Crea una rama nueva (`git checkout -b feature/tu-caracteristica`).
3. Realiza tus cambios y haz **commit** (`git commit -m "Agregar característica X"`).
4. Haz **push** de tu rama (`git push origin feature/tu-caracteristica`).
5. Abre un **Pull Request** en GitHub.

Asegúrate de mantener buenas prácticas de código y documentar claramente tus cambios.

---

## Contacto

Si tienes alguna sugerencia, problema o duda, abre un **issue** en el repositorio:

[👉 Abrir un Issue](https://github.com/gabrielmiguelok/Grabador-PantallaAudio-Linux/issues)

¡Disfruta grabando!

