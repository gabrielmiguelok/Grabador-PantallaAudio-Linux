# user_input.py
#
# Módulo para la interacción con el usuario.
# Solicita:
# - Nombre base de archivo
# - Modo de grabación (pantalla, pantalla+cámara, ventana, ventana+cámara).
#
# El FPS ya no se pregunta; se toma por defecto de config.

def solicitar_opciones_usuario():
    # Pide al usuario el nombre base (sin extensión).
    # Modo de grabación:
    #   1) Pantalla
    #   2) Pantalla + Cámara
    #   3) Ventana
    #   4) Ventana + Cámara
    #
    # Retorna (base_filename, modo).

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

    return base_filename, modo
