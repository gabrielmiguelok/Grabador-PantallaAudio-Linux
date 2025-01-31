# Grabador-PantallaAudio-Linux

## Índice

1. [Descripción](#descripción)
2. [Características](#características)
3. [Requisitos](#requisitos)
4. [Instalación](#instalación)
    - [Instalar Dependencias de Python](#instalar-dependencias-de-python)
    - [Instalar Dependencias del Sistema](#instalar-dependencias-del-sistema)
5. [Uso](#uso)
6. [Contribuciones](#contribuciones)

---

## Descripción

¿Alguna vez quisiste **grabar la pantalla de tu escritorio en Linux** y **mezclar simultáneamente** todo el audio (micrófonos, música, aplicaciones, etc.) en un solo archivo? Este proyecto **Open-Source** es la solución que estabas buscando.

Este script en Python configura automáticamente un **sink nulo** ("combined") y conecta todas las fuentes de audio (micrófonos y monitores) para capturarlas en un **solo stream**. Luego, utiliza **ffmpeg** para grabar la pantalla junto al audio combinado, ahorrándote tiempo y simplificando el proceso de grabación.

> **Repositorio**: [Grabador-PantallaAudio-Linux](https://github.com/gabrielmiguelok/Grabador-PantallaAudio-Linux)
> *(MIT License)*

---

## Características

1. **Configuración Automática de PulseAudio**
    - Crea un **sink nulo** y **loopbacks** necesarios para dirigir todas las fuentes de audio a un mismo canal de grabación.
    - Evita la configuración manual de cada dispositivo.

2. **Grabación Completa con `ffmpeg`**
    - Captura la **pantalla** en la resolución predeterminada (o especificada).
    - Mezcla en tiempo real **todas** las fuentes de audio en un **solo archivo**.

3. **Interfaz Interactiva**
    - Ejecuta el script y responde algunas preguntas mínimas (FPS, nombre de archivo).
    - Limpia automáticamente los módulos de audio al **finalizar** la grabación.

4. **Optimizado para Linux**
    - Utiliza `pactl` para interactuar con PulseAudio (o PipeWire con compatibilidad de Pulse).
    - Se basa en `ffmpeg` para la codificación en h264 + AAC en un contenedor `.mkv`.

5. **Fácil Detención y Post-proceso**
    - Detén la grabación en cualquier momento con Enter (o `Ctrl+C`).
    - El script limpia automáticamente la configuración de audio para no **romper** tu entorno de sonido.

---

## Requisitos

### Dependencias de Python

- **Python 3** (versión >= 3.7)
- **python-xlib**

### Dependencias del Sistema

- **ffmpeg**
- **pulseaudio-utils** (o **pipewire-pulse**, según tu distribución)

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Grabador-PantallaAudio-Linux.git
cd Grabador-PantallaAudio-Linux

### 2. Crear y Activar un Entorno Virtual (Opcional pero Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias de Python

Se proporciona un archivo `requirements.txt` para instalar las dependencias necesarias con `pip`.

```bash
p install -r requirements.txt
```

### 4. Instalar Dependencias del Sistema

### Para **Ubuntu/Debian**

```bash
sudo apt-get update
sudo apt-get install ffmpeg pulseaudio-utils
```

### Para **Arch/Manjaro**

```bash
sudo pacman -S ffmpeg pipewire-pulse
```

### Para Otras Distribuciones

Utiliza el gestor de paquetes de tu distribución para instalar `ffmpeg` y `pulseaudio-utils` o `pipewire-pulse`.

---

## Uso

1. **Ejecuta el Script**

    Asegúrate de estar en el directorio del proyecto o haber instalado el script globalmente si seguiste la opción de `pyproject.toml`.

    ```bash
    python screen_audio_recorder.py
    ```

2. **Proporciona la Información Solicitada**
    - **Tasa de fotogramas (FPS)**: Ingresa el valor deseado o presiona Enter para usar el predeterminado (30 FPS).
    - **Nombre de archivo de salida**: Ingresa el nombre deseado sin extensión o presiona Enter para usar el predeterminado (`grabacion`).
3. **Inicia la Grabación**

    El script configurará automáticamente los módulos de PulseAudio y comenzará a grabar la pantalla junto con todo el audio combinado.

4. **Detén la Grabación**
    - Presiona **Enter** en la terminal donde se está ejecutando el script.
    - O presiona `Ctrl+C` para detener la grabación de manera forzada.
5. **Archivo de Salida**

    El archivo de grabación se guardará en el directorio actual con el nombre especificado y la extensión `.mkv`.


---

## Contribuciones

¡Contribuciones son bienvenidas! Si deseas mejorar este proyecto, por favor sigue estos pasos:

1. **Fork** el repositorio.
2. Crea una nueva **rama** (`git checkout -b feature/nueva-característica`).
3. **Commit** tus cambios (`git commit -m 'Añadir nueva característica'`).
4. **Push** a la rama (`git push origin feature/nueva-característica`).
5. Abre un **Pull Request**.

Asegúrate de seguir las mejores prácticas de código y de documentación.


---

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en [abrir un issue](https://github.com/gabrielmiguelok/Grabador-PantallaAudio-Linux) en el repositorio.

¡Feliz grabación!
