# Movement Alerts (Alertas de Movimiento)

Este script fue desarrollado para detectar movimientos del mercado de criptomonedas en futuros de binance, con este script usted podra tener en vivo y en directo una alerta cuando un crypto activo este teniendo un movimiento inusal tanto al alza o la baja.

**Como usar el script**

- Descargar python [Aqui](https://www.python.org/ "Aqui")
- Descargar y modificar el Archivo, lo puedes modificar con sublime text, o cualquier otro editor de codigo bajo lso parametros que tu quieras.

```python
VOLUMEN = 100000000 # Valoumen minimo a filtrar
VARIACION = 5  # Variacion en los ultimos 30 minutos en porcentaje
VARIACION_100 = 7  # Variacion en los ultimos 30 minutos en porcentaje si tiene menos de 100k de volumen
VARIACION_FAST = 2  # Variacion en los ultimos 2 minutos en porcentaje
```

- Antes de ejecutar el Script deberas instalar la libreria de Python de Binance `pip install -r requirements.txt`
- Una vez guardado el archivo debes ejecutarlo desde una terminal con el siguiente comando:
- Binance
  `python main_binance.py`
- Bybit
  `python main_bybit.py`
