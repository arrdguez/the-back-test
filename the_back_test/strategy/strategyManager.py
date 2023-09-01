import pandas as pd
import structlog

from .default import default

class StrategyManager(object):
    """docstring for StrategyManager"""
    def __init__(self, arg=None):
        super(StrategyManager, self).__init__()
        self.arg = arg
        self.defaul_strategy = default()

    def getStrategyIndicator(self)->list:
        return self.defaul_strategy.indicator

    def strategyCaller(self, oclh):
        self.defaul_strategy.ema_strategy(oclh)
