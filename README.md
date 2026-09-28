# El ahorcado

Juego de adivinanza desarrollado en Python con Tkinter y el patron MVC.
El computador selecciona una palabra relacionada con programacion e
ingenieria de sistemas y el jugador intenta descubrirla letra por letra.

## Ejecucion

Desde la carpeta `ahorcado` generada:

```bash
python main.py
python -m unittest discover tests
```

## Estructura

- `modelo/`: reglas puras, palabra, aciertos, errores y estados finales.
- `vista/`: ventana Tkinter, teclado, etiquetas y dibujo del ahorcado.
- `controlador/`: conecta eventos de la vista con el modelo.
- `tests/`: pruebas unitarias de las reglas del modelo.
- `main.py`: punto de entrada que ensambla las tres capas.

Se aceptan letras con tilde, que se comparan sin tilde, y la letra Ñ.
Las entradas que no sean una sola letra del alfabeto español se ignoran.
