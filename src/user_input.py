#!/usr/bin/env python3
"""
Módulo para la interacción con el usuario.

Solicita información:
- FPS deseados.
- Nombre base del archivo de salida.
- Modo de grabación (pantalla, pantalla+cámara, ventana, ventana+cámara).
"""

def solicitar_opciones_usuario():
    """
    Solicita al usuario:
      - FPS (valor por defecto 30).
      - Nombre base del archivo de salida (por defecto 'grabacion').
      - Modo de grabación:
          1) Pantalla (con audio)
          2) Pantalla (con audio) + cámara (sin audio)
          3) Ventana específica (con audio)
          4) Ventana específica (con audio) + cámara (sin audio)

    Retorna una tupla: (fps, base_filename, modo).
    """
    while True:
        fps_input = input("Ingresa la tasa de fotogramas (FPS, predeterminado 30): ").strip()
        if not fps_input:
            fps = 30
            break
        try:
            fps = int(fps_input)
            break
        except ValueError:
            print("Error: Por favor ingresa un número entero válido.")

    base_filename_input = input(
        "Nombre base de archivo de salida (sin extensión, predeterminado 'grabacion'): "
    ).strip()
    base_filename = base_filename_input if base_filename_input else "grabacion"

    print("\nElige el modo de grabación:")
    print("1) Pantalla (con audio)")
    print("2) Pantalla (con audio) + cámara (sin audio)")
    print("3) Ventana específica (con audio)")
    print("4) Ventana específica (con audio) + cámara (sin audio)")

    while True:
        modo_input = input("Opción (1, 2, 3 o 4): ").strip()
        if modo_input in {'1', '2', '3', '4'}:
            modo = int(modo_input)
            break
        else:
            print("Opción inválida. Debe ser 1, 2, 3 o 4.")

    return fps, base_filename, modo
