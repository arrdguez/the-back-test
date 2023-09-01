#!/usr/bin/python3

import pandas as pd
from finta import TA

class SuperTrend(object):
    """docstring for SuperTrend"""
    def __init__(self, arg = None):
        super(SuperTrend, self).__init__()
        self.arg = arg


    def superTrend(self, df:pd, period:int = 14, mult:float = 1.5) -> pd:

        ohlcv = pd.DataFrame()
        ohlcv['close'] = df['close']
        ohlcv['open'] = df['open']
        ohlcv['hl2'] = (df['high'] + df['low']) / 2
        ohlcv['ATR'] = TA.ATR(df, period)
        ohlcv = ohlcv.fillna(0)

        ohlcv['UPPERBAND'] = ohlcv['hl2'] + (mult * ohlcv['ATR'])
        ohlcv['LOWERBAND'] = ohlcv['hl2'] - (mult * ohlcv['ATR'])
        ohlcv['UP'] = 0.0
        ohlcv['DW'] = 0.0
        ohlcv = ohlcv.fillna(0)
        trend = 'buy'

        for i in range(1, len(ohlcv['close'])):

            if trend == 'buy':
                if (ohlcv.loc[i,"LOWERBAND"] <= ohlcv.loc[i-1,"LOWERBAND"]) and (ohlcv.loc[i - 1,"DW"] <= ohlcv.loc[i,"close"]):
                    ohlcv.loc[i, 'DW'] = ohlcv.loc[i-1,"DW"]
                    ohlcv.loc[i, 'UP'] = -1
                elif (ohlcv.loc[i,"LOWERBAND"] <= ohlcv.loc[i-1,"LOWERBAND"]) and (ohlcv.loc[i - 1,"DW"] > ohlcv.loc[i,"close"]):
                    ohlcv.loc[i, 'UP'] = ohlcv.loc[i,"UPPERBAND"]
                    trend = 'sell'
                elif (ohlcv.loc[i,"LOWERBAND"] >= ohlcv.loc[i-1,"LOWERBAND"]) and (ohlcv.loc[i - 1,"DW"] <= ohlcv.loc[i,"close"]) and (ohlcv.loc[i,"LOWERBAND"] < ohlcv.loc[i-1, 'DW']):
                    ohlcv.loc[i, 'DW'] = ohlcv.loc[i - 1,"DW"]
                    ohlcv.loc[i, 'UP'] = -1
                else:
                    ohlcv.loc[i, 'DW'] = ohlcv.loc[i,"LOWERBAND"]
                    ohlcv.loc[i, 'UP'] = -1

            if trend == 'sell':
                if (ohlcv.loc[i,"UPPERBAND"] > ohlcv.loc[i-1,"UPPERBAND"]) and (ohlcv.loc[i - 1,"UP"] >= ohlcv.loc[i,"close"]):
                    ohlcv.loc[i, 'UP'] = ohlcv.loc[i-1,"UP"]
                    ohlcv.loc[i, 'DW'] = -1
                elif (ohlcv.loc[i,"UPPERBAND"] > ohlcv.loc[i-1,"UPPERBAND"]) and (ohlcv.loc[i - 1,"UP"] < ohlcv.loc[i,"close"]):
                    ohlcv.loc[i, 'DW'] = ohlcv.loc[i,"LOWERBAND"]
                    ohlcv.loc[i, 'UP'] = -1
                    trend = 'buy'
                elif (ohlcv.loc[i,"UPPERBAND"] <= ohlcv.loc[i-1,"UPPERBAND"]) and (ohlcv.loc[i - 1,"UP"] >= ohlcv.loc[i,"close"]) and (ohlcv.loc[i,"UPPERBAND"] > ohlcv.loc[i-1,"UP"]):
                    ohlcv.loc[i, 'UP'] = ohlcv.loc[i-1,"UP"]
                    ohlcv.loc[i, 'DW'] = -1
                else:
                    ohlcv.loc[i, 'UP'] = ohlcv.loc[i,"UPPERBAND"]
                    ohlcv.loc[i, 'DW'] = -1

        del ohlcv["ATR"]
        del ohlcv["hl2"]
        del ohlcv["UPPERBAND"]
        del ohlcv["LOWERBAND"]
        #del ohlcv["UP"]
        #del ohlcv["date"]
        #del ohlcv["volume"]


        ohlcv = ohlcv.fillna(0)
        ohlcv2 = pd.DataFrame()
        ohlcv2['UP'] = ohlcv['UP']
        ohlcv2['DW'] = ohlcv['DW']
        print(ohlcv2)

        return ohlcv2


