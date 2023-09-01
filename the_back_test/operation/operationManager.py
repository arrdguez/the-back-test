import pandas as pd
import structlog

class OperationManager(object):
    """docstring for OperationManager"""
    def __init__(self, arg=None):
        super(OperationManager, self).__init__()
        self.arg = arg

    def defaultOperation(self, oclh:pd):
        print("defaultOperation")

        statistic = {
            "buy":0
        }
        columnsName = ['date', 'open', 'slp']


        insideMarket = False

        for i in range(1, len(oclh['close'])):
            if oclh['strategysignals'].iat[i] == 'buy' and insideMarket == False and (oclh['strategysignals'].iat[i-2] == 'wait' or oclh['strategysignals'].iat[i-2] == 'sell'):
                insideMarket = True
            if oclh['strategysignals'].iat[i] == 'sell' and insideMarket == False and  (oclh['strategysignals'].iat[i-2] == 'wait' or oclh['strategysignals'].iat[i-2] == 'buy'):
                insideMarket = True
