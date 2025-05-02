import pandas as pd
import structlog
from finta import TA


class default(object):
    """
        Simple ema strategy.
    """
    def __init__(self, arg = None):
        super(default, self).__init__()
        self.arg = arg
        self.indicator = [
            ("ema",10),
            ("ema",55)
            ]

    def setup(self, oclh:pd)->pd:
        #logger.info(f"{i[0]} period {i[1]}")
        self.oclh["ema10"] = TA.SMA(self.df, int(10), "close")
        self.oclh["ema55"] = TA.SMA(self.df, int(55), "close")
        return oclh



    def ema_strategy(self, oclh:pd)->pd:
        oclh['strategysignals'] = ""


        for i in range(1, len(oclh['close'])):
            #print(oclh['ema10'].iat[i])
            if oclh['ema10'].iat[i-1] > oclh['ema55'].iat[i-1]:
                oclh['strategysignals'].iat[i-1] = 'buy'
            elif oclh['ema10'].iat[i-1] < oclh['ema55'].iat[i-1]:
                oclh['strategysignals'].iat[i-1] = 'sell'
            else:
                oclh['strategysignals'].iat[i-1] = 'wait'




        return oclh
