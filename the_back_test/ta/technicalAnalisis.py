import pandas as pd
import structlog
from finta import TA

from .SMI import SMIHistogram
from .SMI import ADX
from .SMI import ATR

from .supertrend import SuperTrend


class TechnicalAnalisis(object):
    """docstring for TechnicalAnalisis"""
    def __init__(self, arg = None):
        super(TechnicalAnalisis, self).__init__()
        self.arg = arg
        self.df = pd.DataFrame()

    def getData(self, df:pd):
        self.df = df


    def TechnicalAnalisis(self, df:pd = None, indicators:list=None):
        logger = structlog.get_logger(__name__)
        logger.info("Technical Analysis")

        if indicators == None:
            indicators:list=[("sma",10)]

        if df.empty:
            self.df = df

        for i in indicators:
            if i[0] == "sma":
                logger.info(f"{i[0]} period {i[1]}")
                self.df[i[0]+str(i[1])] = TA.SMA(self.df, int(i[1]),"close")

            if i[0] == "ema":
                logger.info(f"{i[0]} period {i[1]}")
                self.df[i[0]+str(i[1])] = TA.EMA(self.df, int(i[1]),"close")

            if i[0] == "rsi":
                logger.info(f"{i[0]} period {i[1]}")
                self.df[i[0]+str(i[1])] = TA.RSI(self.df, int(i[1]),"close")

            if i[0] == "smih":
                logger.info(f"{i[0]} period {i[1]}")
                objeto = SMIHistogram()
                self.df[i[0]+str(i[1])] = objeto.SMIH(self.df, int(i[1]))

            if i[0] == "supertrend":
                logger.info(f"{i[0]}, period {i[1]}, multiplier {i[2]}.")
                objeto = SuperTrend()
                df2 = objeto.superTrend(self.df, int(i[1]), float(i[2]))
                self.df["UP"+str(i[1])] = df2["UP"]
                self.df["DW"+str(i[1])] = df2["DW"]

        return self.df




    def adx(self):
        adx = ADX()

    def atr(self):
        atr = ATR()

    def smih(self):
        smih = SMIHistogram()
