"""Pruebas unitarias de las reglas de El ahorcado."""

import unittest

from modelo.juego import JuegoAhorcado, normalizar_texto


class TestJuegoAhorcado(unittest.TestCase):
    def juego(self, palabra="PYTHON"):
        return JuegoAhorcado(palabra=palabra)

    def test_acierto_revela_letra(self):
        juego = self.juego()
        self.assertEqual(juego.probar_letra("P"), "acierto")
        self.assertEqual(juego.palabra_visible, "P _ _ _ _ _")

    def test_error_registra_letra(self):
        juego = self.juego()
        self.assertEqual(juego.probar_letra("Z"), "error")
        self.assertEqual(juego.errores, 1)
        self.assertEqual(juego.letras_falladas, ["Z"])

    def test_letra_repetida_no_suma_error(self):
        juego = self.juego()
        juego.probar_letra("Z")
        self.assertEqual(juego.probar_letra("z"), "repetida")
        self.assertEqual(juego.errores, 1)

    def test_entrada_invalida(self):
        juego = self.juego()
        self.assertEqual(juego.probar_letra("12"), "invalida")
        self.assertEqual(juego.probar_letra(""), "invalida")
        self.assertEqual(juego.errores, 0)

    def test_victoria(self):
        juego = self.juego("SOL")
        for letra in "SOL":
            juego.probar_letra(letra)
        self.assertTrue(juego.ha_ganado)
        self.assertTrue(juego.juego_terminado)

    def test_derrota(self):
        juego = self.juego()
        for letra in "ABCDEZ":
            juego.probar_letra(letra)
        self.assertTrue(juego.ha_perdido)
        self.assertEqual(juego.intentos_restantes, 0)

    def test_normalizacion_de_tildes_y_enie(self):
        self.assertEqual(normalizar_texto("áéíóú"), "AEIOU")
        self.assertEqual(normalizar_texto("ñandú"), "ÑANDU")
        juego = self.juego("ÁRBOL")
        self.assertEqual(juego.probar_letra("á"), "acierto")


if __name__ == "__main__":
    unittest.main()
