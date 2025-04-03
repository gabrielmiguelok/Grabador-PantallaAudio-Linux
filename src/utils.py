#!/usr/bin/env python3
"""
Módulo de utilidades que contiene funciones auxiliares.

Proporciona funciones para detectar la resolución de la pantalla y determinar el display a capturar.
"""

def get_screen_resolution():
    """
    Detecta y retorna la resolución de la pantalla en formato 'anchoxalto'.

    Utiliza el módulo python-xlib. Si no está instalado, muestra un error y finaliza el programa.
    """
    try:
        from Xlib import display
        screen = display.Display().screen()
        width = screen.width_in_pixels
        height = screen.height_in_pixels
        return f"{width}x{height}"
    except ImportError:
        print("Se requiere el módulo python-xlib (pip install python-xlib) para capturar la pantalla en Linux.")
        import sys
        sys.exit(1)

def get_display():
    """
    Retorna la pantalla de captura.

    Por defecto se utiliza ':0.0'. Modificar si el entorno DISPLAY es diferente.
    """
    return ':0.0'
