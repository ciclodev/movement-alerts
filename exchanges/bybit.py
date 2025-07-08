import ccxt.async_support as ccxt

from utils.logger_config import logger
from exchanges.exchange import ExchangeAdapter


class BybitAdapter(ExchangeAdapter):
    def __init__(self):
        self.exchange = ccxt.bybit({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',      # selecciona mercados de futuros
                'defaultSubType': 'linear'
            }
        })
        logger.info(f"Conectado a {self.exchange.name}")

    async def __aenter__(self):
        # Carga mercados una sola vez
        # self.markets = await self.exchange.load_markets()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # Cierra la sesión *una sola vez* al salir del with
        await self.exchange.close()

    async def get_symbols(self):
        markets = await self.exchange.load_markets()
        symbols = [
            market['id']  # O market['symbol'] si quieres el formato 'BTC/USDT'
            # Desempaqueta la tupla (symbol, market_object)
            for _, market in markets.items()
            if market['active'] == True and market['quote'] == 'USDT' and market['linear'] == True and market['info']['status'] == 'Trading'
        ]

        logger.info('Numero de monedas encontradas # ' + str(len(symbols)))
        return sorted(symbols)

    async def get_klines(self, symbol, timeframe='1m', limit=30):
        # Verifica si el símbolo es válido
        if symbol not in await self.exchange.load_markets():
            return []
        klines = await self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return klines

    async def info_ticks(self, symbol):
        info = await self.exchange.fetch_ticker(symbol)
        return info['info']

    async def close(self):
        await self.exchange.close()
