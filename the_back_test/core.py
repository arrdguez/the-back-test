import pandas as pd
import structlog


from exchanges.exchangeManager import exchangeManager
from strategy.strategyManager import StrategyManager
from operation.operationManager import OperationManager
from ta.technicalAnalisis import TechnicalAnalisis
from plot.plot import PlotChart


class Core(object):
    """docstring for Core"""
    def __init__(self, arg=None):
        super(Core, self).__init__()
        self.arg = arg
        self.logger = structlog.get_logger(__name__)
        self.excman = exchangeManager()
        self.stratman = StrategyManager()
        self.opman = OperationManager()
        self.techan = TechnicalAnalisis()
        self.plotman = PlotChart(inputFileName = "./plot/BTCUSDT_4h.csv")
        self.df = pd.DataFrame()

    def getData(self, offline:bool=False):
        if offline:
            self.logger.info(f'Offline mode.')
            self.df = pd.read_csv("./downloads/default_BTCUSDT_4h.csv")
        else:

            self.df = self.excman.getData(exchange="Binance", symbol="BTCUSDT", interval="4h", export=False)


    def taCalc(self, indicators:list=[("ema",10)]):

        self.techan.getData(self.df)

        #indicators =  indicators+[("supertrend",14,1.5)]
        self.df = self.techan.TechnicalAnalisis(df = self.df, indicators = indicators)


    def printData(self):
        print(self.df)

    def backTesting(self):
        indicators = self.stratman.getStrategyIndicator()
        self.taCalc(indicators)
        self.stratman.strategyCaller(self.df)
        self.opman.defaultOperation(self.df)


    def cleaner(self):
        """
            The cleaner is an artifact to remove
            all temporal files created in the process.
        """



def main():
    core = Core()
    core.getData()
    core.taCalc()

    core.printData()
    core.backTesting()

if __name__ == '__main__':
    main()
