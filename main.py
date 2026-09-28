"""Punto de entrada de la aplicación El ahorcado."""

import tkinter as tk

from controlador.controlador import ControladorAhorcado
from modelo.juego import JuegoAhorcado
from vista.interfaz import AhorcadoUI


def main():
    """Construye las capas MVC e inicia el bucle de Tkinter."""
    raiz = tk.Tk()
    vista = AhorcadoUI(raiz)
    modelo = JuegoAhorcado()
    ControladorAhorcado(modelo, vista)
    raiz.mainloop()


if __name__ == "__main__":
    main()
