from abc import ABC, abstractmethod

class ExchangeAdapter(ABC):
    @abstractmethod
    async def get_symbols(self):
        pass

    @abstractmethod
    async def get_klines(self, symbol, timeframe='1m', limit=30):
        pass

    @abstractmethod
    async def info_ticks(self, symbol):
        pass

    @abstractmethod
    async def close(self):
        pass
