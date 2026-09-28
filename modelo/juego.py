"""Logica pura del juego El ahorcado, sin dependencias graficas."""

import random
import unicodedata


PALABRAS = (
    "ALGORITMO", "PYTHON", "VARIABLE", "FUNCION", "CLASE",
    "OBJETO", "HERENCIA", "RECURSION", "BASEDEDATOS", "SERVIDOR",
    "CLIENTE", "REDES", "SISTEMA", "SOFTWARE", "HARDWARE",
    "COMPILADOR", "INTERFAZ", "PUNTERO", "MATRIZ", "CIBERSEGURIDAD",
    "CRIPTOGRAFIA", "NUBE", "DEPURADOR", "PROGRAMACION", "INGENIERIA",
    "ARQUITECTURA", "PROTOCOLO", "ESTRUCTURA", "CONCURRENCIA", "ÑANDU",
)


def normalizar_texto(texto):
    """Convierte a mayusculas y elimina tildes, conservando la Ñ."""
    protegido = texto.replace("Ñ", "\x00").replace("ñ", "\x00")
    descompuesto = unicodedata.normalize("NFD", protegido)
    sin_tildes = "".join(
        caracter
        for caracter in descompuesto
        if unicodedata.category(caracter) != "Mn"
    )
    return sin_tildes.replace("\x00", "Ñ").upper()


class JuegoAhorcado:
    """Mantiene el estado y las reglas de una partida."""

    MAX_ERRORES = 6

    def __init__(self, palabras=None, palabra=None):
        """Inicia una partida con una palabra aleatoria o indicada."""
        opciones = tuple(palabras or PALABRAS)
        if not opciones:
            raise ValueError("Debe existir al menos una palabra.")
        self.palabra = normalizar_texto(palabra or random.choice(opciones))
        if not self.palabra.isalpha():
            raise ValueError("La palabra solo puede contener letras.")
        self.letras_acertadas = set()
        self.letras_falladas = []

    @property
    def errores(self):
        """Devuelve el numero de intentos incorrectos."""
        return len(self.letras_falladas)

    @property
    def intentos_restantes(self):
        """Devuelve cuantos errores quedan antes de perder."""
        return self.MAX_ERRORES - self.errores

    def probar_letra(self, letra):
        """Procesa una letra y devuelve su resultado descriptivo."""
        letra_normalizada = normalizar_texto(letra)
        if len(letra_normalizada) != 1 or not (
            "A" <= letra_normalizada <= "Z" or letra_normalizada == "Ñ"
        ):
            return "invalida"
        if self.juego_terminado:
            return "terminado"
        if letra_normalizada in self.letras_acertadas or letra_normalizada in self.letras_falladas:
            return "repetida"
        if letra_normalizada in self.palabra:
            self.letras_acertadas.add(letra_normalizada)
            return "acierto"
        self.letras_falladas.append(letra_normalizada)
        return "error"

    @property
    def palabra_visible(self):
        """Devuelve la palabra con guiones para letras no descubiertas."""
        return " ".join(
            letra if letra in self.letras_acertadas else "_"
            for letra in self.palabra
        )

    @property
    def ha_ganado(self):
        """Indica si todas las letras de la palabra fueron descubiertas."""
        return all(letra in self.letras_acertadas for letra in self.palabra)

    @property
    def ha_perdido(self):
        """Indica si se alcanzaron los seis errores permitidos."""
        return self.errores >= self.MAX_ERRORES

    @property
    def juego_terminado(self):
        """Indica si la partida ya tiene un resultado final."""
        return self.ha_ganado or self.ha_perdido
