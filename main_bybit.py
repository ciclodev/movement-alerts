import asyncio

from colorama import Fore
from exchanges.bybit import BybitAdapter
from strategies.klines_percent import process_single_symbol
from utils.console import clear_console
from utils.constants import *
from utils.format_utils import human_format
from utils.logger_config import logger


async def main():
    clear_console()
    logger.info(f'=== Bot {BOT_NAME} Started ===',
                extra={'color': Fore.YELLOW})

    # Ya no hay finally ni close manual:
    async with BybitAdapter() as exchange:
        symbols = await exchange.get_symbols()
        contador = 1
        try:
            while True:
                logger.info(f'Iniciando ciclo {contador}', extra={
                            'color': Fore.YELLOW})
                await asyncio.gather(*(process_single_symbol(exchange, s) for s in symbols))
                logger.info(f'Fin ciclo {contador}',
                            extra={'color': Fore.YELLOW})
                contador += 1
                await asyncio.sleep(TIME_TO_SLEEP)
        except KeyboardInterrupt:
            logger.warning('Bot detenido por el usuario.')

    logger.info(f'=== Bot {BOT_NAME} Finish ===', extra={'color': Fore.YELLOW})


if (__name__ == "__main__"):
    clear_console()
    asyncio.run(main())
