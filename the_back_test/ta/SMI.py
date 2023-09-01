#!/usr/bin/python3

import pandas as pd
import numpy as np
from finta import TA
from sklearn.linear_model import LinearRegression
import structlog


class SMIHistogram():
    """docstring for smiHistogram"""
    def __init__(self):
      self.logger = structlog.get_logger(__name__)

    def SMIH(self, df, kclength:int = 18) -> pd:

        #self.logger.info(f'Calculating Squeez Momentum Indicator Histogram: KC length:{kclength}')

        dfTem = pd.DataFrame()
        dfTem['close'] = df['close']
        dfTem['sma'] =  df['close'].rolling(window = kclength).mean()
        dfTem['highest'] = df["high"].rolling(center=False, window = kclength).max()
        dfTem['lowest'] = df["low"].rolling(center=False, window = kclength).min()
        dfTem['aveHL'] = (dfTem['lowest'] + dfTem['highest'])/2
        dfTem['aveHLS'] = (dfTem['aveHL'] + dfTem['sma'])/2
        dfTem['source'] = df['close'] - dfTem['aveHLS']
        dfTem = dfTem.fillna(0)

        yAll = dfTem['source'].values.tolist()
        x = np.array(list(range(1, kclength+1))).reshape((-1, 1))

        SMH = []
        for i in range(len(dfTem['close'])-1,kclength*2,-1):
            y = np.array(yAll[i-kclength+1:i+1])
            reg = LinearRegression(fit_intercept = True).fit(x, y)
            SMH.append(reg.predict(x)[-1 ])

        tmp = [0 for _ in range(len(yAll)-len(SMH))]
        SMH = SMH + tmp

        SMH.reverse()

        return pd.Series(SMH, name="{0} period SMA".format(kclength))


        return df


class ADX():
    """docstring for smiHistogram"""
    def __init__(self):
      self.logger = structlog.get_logger(__name__)

    def adx(self, df, period:int = 14, adxlen:int = 14) -> pd:
        self.logger.info(f'Calculating the ADX: Period: {period}, ADX length: {adxlen}.')

        dfTmp = pd.DataFrame()
        #dfTmp = df
        dfTmp['open'] = df['open']
        dfTmp['high'] = df['high']
        dfTmp['low'] = df['low']
        dfTmp['close'] = df['close']
        dfTmp['up'] = df['high'].diff()
        dfTmp['down'] = -df['low'].diff()
        dfTmp['up'] = dfTmp['up'].fillna(0)
        dfTmp['down'] = dfTmp['down'].fillna(0)
        dfTmp['TR'] = TA.TR(df)
        dfTmp['truerange'] = TA.SMMA( dfTmp, period = 14, column = "TR", adjust = True)
        dfTmp['date']= pd.to_datetime(df['date'])
        df = df.fillna(0)
        dfTmp = dfTmp.fillna(0)

        for i in range(0, len(dfTmp['close'])):
            if (dfTmp.loc[i,"up"] > dfTmp.loc[i,"down"]) & (dfTmp.loc[i,"up"] > 0):
                dfTmp.loc[i, 'plus'] = dfTmp.loc[i, 'up']
            else:
                dfTmp.loc[i, 'plus'] = 0
            if (dfTmp.loc[i,"down"] > dfTmp.loc[i,"up"]) & (dfTmp.loc[i,"down"] > 0):
                dfTmp.loc[i, 'minus'] = dfTmp.loc[i, 'down']
            else:
                dfTmp.loc[i, 'minus'] = 0

        dfTmp['plus'] = dfTmp['plus'].fillna(0)
        dfTmp['minus'] = dfTmp['minus'].fillna(0)

        dfTmp['plus'] = TA.SMMA(dfTmp, period=14, column='plus', adjust=True)
        dfTmp['minus'] = TA.SMMA(dfTmp, period=14, column='minus', adjust=True)

        dfTmp['plus'] = 100 * dfTmp['plus'] / dfTmp['truerange']
        dfTmp['minus'] = 100 * dfTmp['minus'] / dfTmp['truerange']

        dfTmp['sum'] = dfTmp['minus'] + dfTmp['plus']

        for i in range(0, len(dfTmp['sum'])):
          if float(dfTmp.loc[i,'sum']) == 0:
              dfTmp.loc[i,'tmp'] = abs(dfTmp.loc[i,'plus'] - dfTmp.loc[i,'minus']) / 1
          else:
              dfTmp.loc[i,'tmp'] = abs(dfTmp.loc[i,'plus'] - dfTmp.loc[i,'minus']) / dfTmp.loc[i,'sum']

        dfTmp['ADX'] =100 * TA.SMMA(dfTmp, period=adxlen, column='tmp', adjust=True)

        df['ADX'] = dfTmp['ADX']

        return df


class ATR():
    """docstring for smiHistogram"""
    def __init__(self):
      self.logger = structlog.get_logger(__name__)

    def atr(self, df, last:bool = False) -> pd:
        self.logger.info("Calculating the ATR ... ")

        df['ATR'] = TA.ATR(df)
        df['ATR'] = df['ATR'].fillna(0)
        if last:
            return float(df['ATR'].iat[-1])
        else:
            return df

def main():
    pass


if __name__ == "__main__":
    main()
