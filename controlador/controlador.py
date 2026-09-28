"""Conecta los eventos de la vista con el modelo."""

from modelo.juego import normalizar_texto


class ControladorAhorcado:
    """Coordina una partida sin dibujar ni almacenar reglas graficas."""

    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.vista.callback_letra = self.procesar_letra
        self.vista.callback_nueva = self.nueva_partida
        self.actualizar_vista()

    def procesar_letra(self, entrada):
        """Valida indirectamente mediante el modelo y actualiza la vista."""
        letra = normalizar_texto(entrada)
        resultado = self.modelo.probar_letra(entrada)
        if len(letra) == 1:
            self.vista.deshabilitar_letra(letra)
        if resultado == "invalida":
            self.vista.mostrar_mensaje_final("Introduce una sola letra valida.", True)
            return
        self.actualizar_vista()
        if self.modelo.ha_ganado:
            self.vista.mostrar_mensaje_final(
                f"Ganaste. La palabra era: {self.modelo.palabra}", True
            )
        elif self.modelo.ha_perdido:
            self.vista.mostrar_mensaje_final(
                f"Perdiste. La palabra era: {self.modelo.palabra}", False
            )

    def nueva_partida(self):
        """Crea un modelo nuevo y restablece todos los controles."""
        self.modelo.__init__()
        self.vista.reiniciar()
        self.actualizar_vista()

    def actualizar_vista(self):
        """Sincroniza los datos visibles con el estado del modelo."""
        self.vista.mostrar_palabra(self.modelo.palabra_visible)
        self.vista.mostrar_errores(self.modelo.letras_falladas)
        self.vista.mostrar_intentos(self.modelo.intentos_restantes)
        self.vista.dibujar_muñeco(self.modelo.errores)
