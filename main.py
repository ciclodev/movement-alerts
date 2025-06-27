import logging
import sys
import time

from binance.client import Client
from colorama import Fore, init
from color import ColorFormatter

BOT_NAME = "Movement Alerts"
VARIACION = 5  # Variacion en los ultimos 30 minutos en porcentaje
# Variacion en los ultimos 30 minutos en porcentaje si tiene menos de 100k de volumen
VARIACION_100 = 7
VARIACION_FAST = 2  # Variacion en los ultimos 2 minutos en porcentaje
VOLUMEN = 100000000  # Minimo

client = Client()
init(autoreset=True)
logger = logging.getLogger("bot_movement-alerts")
logger.setLevel(logging.INFO)
logger.propagate = False          # ¡corta la subida al root!

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter(
    "%(asctime)s - [%(levelname)s] %(message)s"))
logger.addHandler(handler)


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
                logger.info('=' * 50)
                logger.info('LONG: '+symbol, extra={'color': Fore.GREEN})
                logger.info('Variacion: ' + str(result) +
                            '%', extra={'color': Fore.GREEN})
                logger.info('Volumen: ' + human_format(volumen),
                            extra={'color': Fore.GREEN})
                logger.info('Precio max: ' +
                            info['highPrice'], extra={'color': Fore.GREEN})
                logger.info('Precio min: ' +
                            info['lowPrice'], extra={'color': Fore.GREEN})
                logger.info('=' * 50)

    # SHORT
    if final > inicial:
        result = round(((final - inicial) / inicial) * 100, 2)
        if result >= VARIACION:
            info = info_ticks(symbol)
            volumen = float(info['quoteVolume'])
            if volumen > VOLUMEN or result >= VARIACION_100:
                logger.info('=' * 50)
                logger.info('SHORT: ' + symbol, extra={'color': Fore.RED})
                logger.info('Variacion: ' + str(result) +
                            '%', extra={'color': Fore.RED})
                logger.info('Volumen: ' + human_format(volumen),
                            extra={'color': Fore.RED})
                logger.info('Precio max: ' +
                            info['highPrice'], extra={'color': Fore.RED})
                logger.info('Precio min: ' +
                            info['lowPrice'], extra={'color': Fore.RED})
                logger.info('=' * 50)

    # FAST
    if knumber >= 3:
        inicial = float(klines[knumber-2][4])
        final = float(klines[knumber][4])
        if inicial < final:
            result = round(((final - inicial) / inicial) * 100, 2)
            if result >= VARIACION_FAST:
                info = info_ticks(symbol)
                volumen = float(info['quoteVolume'])
                logger.info('=' * 50)
                logger.info('FAST SHORT!: ' + symbol,
                            extra={'color': Fore.RED})
                logger.info('Variacion: ' + str(result) +
                            '%', extra={'color': Fore.RED})
                logger.info('Volumen: ' + human_format(volumen),
                            extra={'color': Fore.RED})
                logger.info('Precio max: ' +
                            info['highPrice'], extra={'color': Fore.RED})
                logger.info('Precio min: ' +
                            info['lowPrice'], extra={'color': Fore.RED})


def main():
    try:
        logger.info(f'=== Bot {BOT_NAME} Started ===',
                    extra={'color': Fore.YELLOW})
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
        logger.info(f'=== GridBot {BOT_NAME} Finish ===', extra={
                    'color': Fore.YELLOW})


if (__name__ == "__main__"):
    main()
