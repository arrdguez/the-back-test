import pandas as pd
import structlog


from .binanceExc import Binance


class exchangeManager(object):
    """docstring for exchangeManager"""
    def __init__(self, arg=None):
        super(exchangeManager, self).__init__()
        self.arg = arg
        self.binance = Binance()

    def getData(self, symbol:str, interval:str, exchange:str="Binance", export:bool=True):

        if exchange == "Binance":
            return self.binance.exportKlines(symbol=symbol, interval=interval, export=export)




def main():
    exm = exchangeManager()

if __name__ == '__main__':
    main()
