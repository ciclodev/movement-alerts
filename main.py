import logging
import time
from binance.client import Client

BOT_NAME = "Movement Alerts"
VARIACION = 5  # Variacion en los ultimos 30 minutos en porcentaje
# Variacion en los ultimos 30 minutos en porcentaje si tiene menos de 100k de volumen
VARIACION_100 = 7
VARIACION_FAST = 2  # Variacion en los ultimos 2 minutos en porcentaje
VOLUMEN = 100000000  # Minimo

client = Client()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("bot_movement-alerts")


def get_symbols():
    # trae todas las monedas de futuros de binace
    result = client.futures_exchange_info()

    # Filtra la que sean USDT y que esten en estatus TRADING
    symbols = [
        d['symbol']
        for d in result['symbols']
        if d.get('status') == 'TRADING' and d.get('quoteAsset') == 'USDT'
    ]

    logger.info('Numero de monedas encontradas # ' + str(len(symbols)))
    return symbols


def get_klines(symbol):
    klines = client.futures_klines(
        symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=30)
    return klines


def info_ticks(symbol):
    info = client.futures_ticker(symbol=symbol)
    return info


def human_format(volumen):
    magnitude = 0
    while abs(volumen) >= 1000:
        magnitude += 1
        volumen /= 1000.0
    return '%.2f%s' % (volumen, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def klines_percent(symbol, klines, knumber):
    inicial = float(klines[0][4])
    final = float(klines[knumber][4])

    # LONG
    if inicial > final:
        result = round(((inicial - final) / inicial) * 100, 2)
        if result >= VARIACION:
            info = info_ticks(symbol)
            volumen = float(info['quoteVolume'])
            if volumen > VOLUMEN or result >= VARIACION_100:
                logger.info('LONG: '+symbol)
                logger.info('Variacion: ' + str(result) + '%')
                logger.info('Volumen: ' + human_format(volumen))
                logger.info('Precio max: ' + info['highPrice'])
                logger.info('Precio min: ' + info['lowPrice'])

    # SHORT
    if final > inicial:
        result = round(((final - inicial) / inicial) * 100, 2)
        if result >= VARIACION:
            info = info_ticks(symbol)
            volumen = float(info['quoteVolume'])
            if volumen > VOLUMEN or result >= VARIACION_100:
                logger.info('SHORT: ' + symbol)
                logger.info('Variacion: ' + str(result) + '%')
                logger.info('Volumen: ' + human_format(volumen))
                logger.info('Precio max: ' + info['highPrice'])
                logger.info('Precio min: ' + info['lowPrice'])

    # FAST
    if knumber >= 3:
        inicial = float(klines[knumber-2][4])
        final = float(klines[knumber][4])
        if inicial < final:
            result = round(((final - inicial) / inicial) * 100, 2)
            if result >= VARIACION_FAST:
                info = info_ticks(symbol)
                volumen = float(info['quoteVolume'])
                logger.info('FAST SHORT!: ' + symbol)
                logger.info('Variacion: ' + str(result) + '%')
                logger.info('Volumen: ' + human_format(volumen))
                logger.info('Precio max: ' + info['highPrice'])
                logger.info('Precio min: ' + info['lowPrice'])


def main():
    try:
        logger.info(f'=== Bot {BOT_NAME} Started ===')
        # Solo se trae una vez
        symbols = get_symbols()
        while True:
            logger.info('Escaneando monedas...')
            for symbol in symbols:
                klines = get_klines(symbol)
                knumber = len(klines)
                if knumber > 0:
                    knumber = knumber - 1
                    klines_percent(symbol, klines, knumber)
            logger.info('Esperando 30 segundos...')
            time.sleep(30)
    except KeyboardInterrupt:
        logger.warning('Bot detenido por el usuario.')
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
    finally:
        logger.info(f'=== GridBot {BOT_NAME} Finish ===')


if (__name__ == "__main__"):
    main()
