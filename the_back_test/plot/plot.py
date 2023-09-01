import plotly.graph_objects as go
from plotly.offline import plot

import pandas as pd
from datetime import datetime


class PlotChart():
    """docstring for PlotChart"""
    def __init__(self, arg=None, inputFileName:str=None):
        super(PlotChart, self).__init__()
        self.arg = arg

        self.df = pd.read_csv(inputFileName)

        # plot candlestick chart
        self.candles = go.Candlestick(
            x=self.df['date'],
            open=self.df['open'],
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'],
            name = "Candlesticks"
            )

    def basicPlot(self):


        fsma = go.Scatter(
            x = self.df['time'],
            y = self.df['close'],
            name = "Test",
            line = dict(color = ('rgba(102, 207, 255, 50)')))

        data = [self.candles, fsma]
        # style and display
        layout = go.Layout(title = "Example Plot")
        fig = go.Figure(data = data, layout = layout)
        filename = "./ExamplePlot.html"
        fig.write_html(filename)


    def plotIndicatorList(self, indicatorList:list):

        data = [self.candles] + indicatorList
        #data.append(indicatorList)

        # style and display
        layout = go.Layout(title = "Example Plot")
        fig = go.Figure(data = data, layout = layout)
        filename = "./ExamplePlot.html"
        fig.write_html(filename)



def main():
    pc = PlotChart("./BTCUSDT_4h.csv")
    pc.basicPlot()


    """
    Testing Indicators
    """

    # plot MAs
    fsma = go.Scatter(
      x = pc.df['time'],
      y = pc.df['close'],
      name = "Test",
      line = dict(color = ('rgba(102, 207, 255, 50)')))
    indic = [fsma]

    pc.plotIndicatorList(indic)

if __name__ == '__main__':
    main()
