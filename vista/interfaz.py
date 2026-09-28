"""Interfaz grafica de El ahorcado; no contiene reglas del juego."""

import tkinter as tk
from tkinter import ttk


LETRAS = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


class AhorcadoUI:
    """Construye widgets y expone operaciones visuales al controlador."""

    def __init__(self, raiz, callback_letra=None, callback_nueva=None):
        self.raiz = raiz
        self.raiz.title("El ahorcado")
        self.raiz.resizable(False, False)
        self.callback_letra = callback_letra
        self.callback_nueva = callback_nueva
        self.botones_letras = {}
        self._construir_widgets()
        self.raiz.bind("<Key>", self._evento_teclado)

    def _construir_widgets(self):
        """Crea el tablero, el canvas y los controles."""
        marco = ttk.Frame(self.raiz, padding=16)
        marco.grid(row=0, column=0)
        ttk.Label(marco, text="EL AHORCADO", font=("TkDefaultFont", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 12)
        )
        self.canvas = tk.Canvas(marco, width=280, height=260, bg="white", highlightthickness=1)
        self.canvas.grid(row=1, column=0, rowspan=4, padx=(0, 16))
        panel = ttk.Frame(marco)
        panel.grid(row=1, column=1, sticky="n")
        self.etiqueta_palabra = ttk.Label(panel, text="_", font=("TkDefaultFont", 20, "bold"))
        self.etiqueta_palabra.grid(row=0, column=0, pady=(0, 12))
        self.etiqueta_fallos = ttk.Label(panel, text="Letras falladas: -")
        self.etiqueta_fallos.grid(row=1, column=0, sticky="w")
        self.etiqueta_intentos = ttk.Label(panel, text="Intentos restantes: 6")
        self.etiqueta_intentos.grid(row=2, column=0, sticky="w", pady=(4, 12))
        self.etiqueta_mensaje = ttk.Label(panel, text="", foreground="#14532d", wraplength=240)
        self.etiqueta_mensaje.grid(row=3, column=0, pady=(0, 8))
        teclado = ttk.Frame(panel)
        teclado.grid(row=4, column=0)
        for indice, letra in enumerate(LETRAS):
            boton = ttk.Button(teclado, text=letra, width=3, command=lambda l=letra: self._clic_letra(l))
            boton.grid(row=indice // 7, column=indice % 7, padx=2, pady=2)
            self.botones_letras[letra] = boton
        self.boton_nueva = ttk.Button(panel, text="Nueva partida", command=self._clic_nueva)
        self.boton_nueva.grid(row=5, column=0, pady=(12, 0))

    def _clic_letra(self, letra):
        if self.callback_letra:
            self.callback_letra(letra)

    def _evento_teclado(self, evento):
        """Reenvia al controlador las teclas fisicas pulsadas."""
        if self.callback_letra and evento.char:
            self.callback_letra(evento.char)

    def _clic_nueva(self):
        if self.callback_nueva:
            self.callback_nueva()

    def mostrar_palabra(self, palabra):
        self.etiqueta_palabra.config(text=palabra)

    def mostrar_errores(self, errores):
        self.etiqueta_fallos.config(text="Letras falladas: " + (", ".join(errores) or "-"))

    def mostrar_intentos(self, restantes):
        self.etiqueta_intentos.config(text=f"Intentos restantes: {restantes}")

    def dibujar_muñeco(self, errores):
        """Dibuja progresivamente la horca y las seis partes del muñeco."""
        self.canvas.delete("all")
        color = "#1f2937"
        self.canvas.create_line(35, 235, 235, 235, fill=color, width=4)
        self.canvas.create_line(75, 235, 75, 35, fill=color, width=4)
        self.canvas.create_line(75, 35, 175, 35, fill=color, width=4)
        self.canvas.create_line(175, 35, 175, 65, fill=color, width=4)
        if errores >= 1:
            self.canvas.create_oval(150, 65, 200, 115, outline=color, width=3)
        if errores >= 2:
            self.canvas.create_line(175, 115, 175, 175, fill=color, width=3)
        if errores >= 3:
            self.canvas.create_line(175, 125, 140, 155, fill=color, width=3)
        if errores >= 4:
            self.canvas.create_line(175, 125, 210, 155, fill=color, width=3)
        if errores >= 5:
            self.canvas.create_line(175, 175, 145, 215, fill=color, width=3)
        if errores >= 6:
            self.canvas.create_line(175, 175, 205, 215, fill=color, width=3)

    def deshabilitar_letra(self, letra):
        letra = letra.upper()
        if letra in self.botones_letras:
            self.botones_letras[letra].state(["disabled"])

    def reiniciar(self):
        for boton in self.botones_letras.values():
            boton.state(["!disabled"])
        self.etiqueta_mensaje.config(text="")

    def mostrar_mensaje_final(self, mensaje, gano):
        self.etiqueta_mensaje.config(text=mensaje, foreground="#14532d" if gano else "#991b1b")
