import asyncio

from colorama import Fore
from utils.constants import *
from utils.format_utils import human_format
from utils.logger_config import logger

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)


async def klines_percent(exchange, symbol, klines):
    knumber = len(klines) - 1
    inicial = float(klines[0][4])
    final = float(klines[knumber][4])

    # LONG
    if inicial > final:
        result = round(((inicial - final) / inicial) * 100, 2)
        if result >= VARIACION:
            info = await exchange.info_ticks(symbol=symbol)
            volumen = float(info['quoteVolume'])
            if volumen > VOLUMEN or result >= VARIACION_100:
                logger.info('=' * 50)
                logger.info(f'LONG: {symbol}', extra={'color': Fore.GREEN})
                logger.info(f'Variacion: {result}%',
                            extra={'color': Fore.GREEN})
                logger.info(f'Volumen: {human_format(volumen)}', extra={
                            'color': Fore.GREEN})
                logger.info(f'Precio max: {info['highPrice']}', extra={
                            'color': Fore.GREEN})
                logger.info(f'Precio min: {info['lowPrice']}', extra={
                            'color': Fore.GREEN})
                logger.info('=' * 50)

    # SHORT
    if final > inicial:
        result = round(((final - inicial) / inicial) * 100, 2)
        if result >= VARIACION:
            info = await exchange.info_ticks(symbol=symbol)
            volumen = float(info['quoteVolume'])
            if volumen > VOLUMEN or result >= VARIACION_100:
                logger.info('=' * 50)
                logger.info(f'SHORT: {symbol}', extra={'color': Fore.RED})
                logger.info(f'Variacion: {result}%', extra={'color': Fore.RED})
                logger.info(f'Volumen: {human_format(volumen)}', extra={
                            'color': Fore.RED})
                logger.info(f'Precio max: {info['highPrice']}', extra={
                            'color': Fore.RED})
                logger.info(f'Precio min: {info['lowPrice']}', extra={
                            'color': Fore.RED})
                logger.info('=' * 50)

    # FAST
    if knumber >= 3:
        inicial = float(klines[knumber-2][4])
        final = float(klines[knumber][4])
        if inicial < final:
            result = round(((final - inicial) / inicial) * 100, 2)
            if result >= VARIACION_FAST:
                info = await exchange.info_ticks(symbol=symbol)
                volumen = float(info['quoteVolume'])
                logger.info('=' * 50)
                logger.info(f'FAST SHORT!: {symbol}',
                            extra={'color': Fore.RED})
                logger.info(f'Variacion: {result}%', extra={'color': Fore.RED})
                logger.info(f'Volumen: {human_format(volumen)}', extra={
                            'color': Fore.RED})
                logger.info(f'Precio max: {info['highPrice']}', extra={
                            'color': Fore.RED})
                logger.info(f'Precio min: {info['lowPrice']}', extra={
                            'color': Fore.RED})
                logger.info('=' * 50)


async def process_single_symbol(exchange, symbol):
    async with semaphore:
        klines = await exchange.get_klines(symbol=symbol)
        if klines:
            logger.info(f"=={symbol}==")
            await klines_percent(exchange=exchange,
                                 symbol=symbol, klines=klines)
