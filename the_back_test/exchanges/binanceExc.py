import requests
import json
import decimal
import pandas as pd
import structlog

request_delay = 1000



class Binance:

    KLINE_INTERVALS = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

    def __init__(self, arg=None, filename=None):
        super(Binance, self).__init__()
        self.arg = arg
        self.logger = structlog.get_logger(__name__)

        self.base = 'https://api.binance.com'
        self.test_base = 'https://testnet.binance.vision'
        self.endpoints = {
          "serverTime"     : '/api/v3/time',
          "klines"         : '/api/v3/klines',
          "exchangeInfo"   : '/api/v3/exchangeInfo',
          "24hrTicker"     : '/api/v3/ticker/24hr',
          "averagePrice"   : '/api/v3/avgPrice',
          "price"          : '/api/v3/ticker/price',
          "orderBook"      : '/api/v3/depth',
          "bestPQOrderBook": '/api/v3/ticker/bookTicker',
        }
        self.headers = {}


    def get(self, url, params=None, headers=None) -> dict:
        """ Makes a Get Request """

        try:
            self.logger.info(f'GET {url}')
            response = requests.get(url, params=params, headers=headers)
            data = json.loads(response.text)
            data['url'] = url
        except Exception as e:
            self.logger.warning("GET method")
            self.logger.warning(f"Exception occurred when trying to access {url}")
            self.logger.warning(e)
            data = {'code': '-1', 'url':url, 'msg': e}

        return data

   #General
    def GET_server_time(self):

        url = self.base + self.endpoints['serverTime']
        return self.get(url, headers=self.headers)

    def GetAvPrice(self, symbol:str):

        url = self.base + self.endpoints['averagePrice']
        params = {
            'symbol': symbol
        }

        return self.get(url, params=params, headers=self.headers)

    def GetPrice(self, symbol:str):

        url = self.base + self.endpoints['price']
        params = {
              'symbol': symbol
        }

        return self.get(url, params=params, headers=self.headers)

    def GetTradingSymbols(self, quoteAssets:list=None):
        '''
          Gets All symbols which are tradable (currently)
        '''

        url = self.base + self.endpoints["exchangeInfo"]

        data = self.get(url)
        if data.__contains__('code'):
            return []

        symbols_list = []
        for pair in data['symbols']:
            if pair['status'] == 'TRADING':
                if quoteAssets != None and pair['quoteAsset'] in quoteAssets:
                  symbols_list.append(pair['symbol'])

        return symbols_list

    def GetSymbolDataOfSymbols(self, symbols:list=None):
        '''
            Gets All symbols which are tradable (currently)
        '''

        url = self.base + self.endpoints["exchangeInfo"]
        data = self.get(url)
        if data.__contains__('code'):
            return []

        symbols_list = []

        for pair in data['symbols']:
            if pair['status'] == 'TRADING':
                if symbols != None and pair['symbol'] in symbols:
                    symbols_list.append(pair)

        return symbols_list

    def GetSymbolKlinesExtra(self, symbol:str, interval:str, limit:int=1000):
        """
            Basically, we will be calling the GetSymbolKlines as many times as we need
            in order to get all the historical data required (based on the limit parameter)
            and we'll be merging the results into one long dataframe.
        """

        repeat_rounds = 0
        if limit > 1000:
            repeat_rounds = int(limit/1000)

        initial_limit = limit % 1000
        if initial_limit == 0:
            initial_limit = 1000

        """
            First, we get the last initial_limit candles, starting at end_time and going
            backwards (or starting in the present moment, if end_time is False)
        """

        df = self.GetSymbolKlines(symbol, interval, limit=initial_limit)

        while repeat_rounds > 0:
            """
                Then, for every other 1000 candles, we get them, but starting at the beginning
                of the previously received candles.
            """

            df2 = self.GetSymbolKlines(symbol, interval, limit=1000, end_time=df['time'][0])
            df = pd.concat([df, df2], ignore_index=True)
            repeat_rounds = repeat_rounds - 1

        return df

    def Get24hrTicker(self, symbol:str):
        url = self.base + self.endpoints['24hrTicker'] + "?symbol="+symbol
        return self.get(url)

    def GetSymbolKlines(self, symbol:str, interval:str, limit:int=1000, init_time=False, end_time=False):
        '''
            Gets trading data for one symbol

            Parameters
            --
              symbol str:        The symbol for which to get the trading data

              interval str:      The interval on which to get the trading data
                minutes      '1m' '3m' '5m' '15m' '30m'
                hours        '1h' '2h' '4h' '6h' '8h' '12h'
                days         '1d' '3d'
                weeks        '1w'
                months       '1M;
        '''
        limitTable = {
            "m1": 0,
            "m3": 0,
            "m5": 0,
            "m15": 0,
            "m30": 0,
            "h1": 0,
            "h2": 0,
            "h4": 0,
            "d1": 0,
            "w1": 0,
        }

        if init_time and end_time:
            if end_time > init_time:
                diff = (end_time - init_time)/1000
                diffMin = diff/60
                limitTable['m1'] = int(diffMin)
                limitTable['m3'] = int(diffMin/3)
                limitTable['m5'] = int(diffMin/5)
                limitTable['m15'] = int(diffMin/15)
                limitTable['m30'] = int(diffMin/30)
                limitTable['h1'] = int(diffMin/60)
                limitTable['h2'] = int(limitTable['h1']/2)
                limitTable['h4'] = int(limitTable['h1']/4)
                limitTable['d1'] = int(limitTable['h1']/24)
                limitTable['w1'] = int(limitTable['d1']/7)
                limit = limitTable[interval[::-1]]
            else:
                logger.error(f'init_time is bigger than end_time. [{init_time}, {end_time}]')



        if limit > 1000:
            return self.GetSymbolKlinesExtra(symbol, interval, limit)

        params = '?&symbol='+symbol+'&interval='+interval+'&limit='+str(limit)


        url = self.base + self.endpoints['klines'] + params

        data = requests.get(url)
        dictionary = json.loads(data.text)
        df = pd.DataFrame.from_dict(dictionary)


        df = df.drop(range(6, 12), axis=1)
        col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
        df.columns = col_names

        for col in col_names:
            df[col] = df[col].astype(float)

        df['date'] = pd.to_datetime(df['time'] * 1000000, infer_datetime_format=True)

        return df

    def GetOrderBook(self, symbol:str, limit:int=100):

        params = {
            'symbol': symbol
        }

        if limit != 100:
            params = {
                'symbol': symbol,
                'limit' : limit
            }

        url = self.base + self.endpoints["orderBook"]

        return self.get(url, params=params, headers=self.headers)

    def GetSortedOrderBook(self, symbol:str="BTCUSDT", limit:int=100)->pd.DataFrame():

        orderBook = self.GetOrderBook(symbol=symbol, limit=limit)
        df = self._df = pd.DataFrame()

        bids = orderBook['bids']
        asks = orderBook['asks'].reverse()


        priceList = []
        qtyList = []

        for x in orderBook['asks']:
            priceList.append(x[0])
            qtyList.append(x[1])

        df['bidsPrice'] = priceList
        df['bidsQty'] = qtyList


        priceList = []
        qtyList = []

        for x in orderBook['bids']:
            priceList.append(x[0])
            qtyList.append(x[1])

        df['asksPrice'] = priceList
        df['asksQty'] = qtyList
        df = df.astype(float)

        return df

    def GETBestPQOrderBook(self, symbol:str):
        """
            Symbol Order Book Ticker
            GET /api/v3/ticker/bookTicker

            Best price/qty on the order book for a symbol or symbols.
        """

        params = {'symbol': symbol}

        url = self.base + self.endpoints["bestPQOrderBook"]

        return self.get(url, params=params, headers=self.headers)

    def GetLotFilte(self, symbol:str) -> dict:
        """
            This function return a dictionary with information about the pair.
            This information will be use to know the correct amount format to trade.
        """

        symbol_data = self.GetSymbolDataOfSymbols([symbol])[0]

        lot_filter = {}
        for fil in symbol_data["filters"]:
            if fil["filterType"] == "LOT_SIZE":
                lot_filter = fil
                break

        return lot_filter

    def GetPriceFilter(self, symbol:str) -> dict:
        """
            This function return a dictionary with information about the pair.
            This information will be use to know the correct amount to spend.
        """

        symbol_data = self.GetSymbolDataOfSymbols([symbol])[0]

        price_filter = {}
        for fil in symbol_data["filters"]:
            if fil["filterType"] == "PRICE_FILTER":
                price_filter = fil
                break

        return price_filter

    def GetMinNotional(self, symbol:str) -> dict:
        """
            This function return a dictionary with information about the pair.
            This information will be use to know the correct amount to spend.
        """

        symbol_data = self.GetSymbolDataOfSymbols([symbol])[0]

        min_notional = {}
        for fil in symbol_data["filters"]:
            if fil["filterType"] == "MIN_NOTIONAL":
                min_notional = fil
                break

        return min_notional

   #Export
    def exportOrderBook(self, symbol:str, limit:int=100):

        orderbook = self.GetOrderBook(symbol, limit)

        bids = orderbook['bids']
        asks = orderbook['asks']
        price = self.GetPrice(symbol)
        newlist = [[price['price'], 0.0000000]]

        df = pd.DataFrame(bids)
        df = df.append(newlist)
        df = df.append(asks)

        df.columns = ['price', 'amount']
        df.sort_values(by=['price'], inplace=True)

        current_time = datetime.datetime.now()
        orderbookfilename = "../"+str(current_time.day)+"."\
                                 +str(current_time.month)+"."\
                                 +str(current_time.year)+"-"\
                                 +str(current_time.hour)+"."\
                                 +str(current_time.minute)+"."\
                                 +str(current_time.second)+"_"\
                                 +symbol+".csv"

        df.to_csv(orderbookfilename)

    def exportKlines(self, symbol:str, interval:str, limit:int=1000, init_time=False, end_time=False, export:bool=True) -> pd:

        df = self.GetSymbolKlines(symbol, interval, limit, init_time, end_time)
        if export:
            fileName = "./downloads/"+symbol+'_'+interval+'.csv'
            df.to_csv(fileName)
        return df


def Main():

    logger = structlog.get_logger(__name__)
    exchange = Binance()

    serverTime = exchange.GET_server_time()['serverTime']
    symbol = 'BTCUSDT'

    #logger.info(f'serverTime: {serverTime}')
    #logger.info(f'GetAvPrice:\n{exchange.GetAvPrice("BTCUSDT")}')
    #logger.info(f'GetPrice:\n{exchange.GetPrice("BTCUSDT")}')
    #logger.info(f'GetTradingSymbols:\n{exchange.GetTradingSymbols("BTC")}')
    #logger.info(f'GetSymbolDataOfSymbols:\n{exchange.GetSymbolDataOfSymbols(symbol)[0]}')
    #logger.info(f'Get24hrTicker:\n{exchange.Get24hrTicker("BTCUSDT")}')
    #logger.info(f'GetSymbolKlines:\n{exchange.GetSymbolKlines("BTCUSDT", "15m", 15)}')
    #logger.info(f'GetOrderBook:\n{exchange.GetOrderBook("BTCUSDT", 10)}')
    #logger.info(f'GetSortedOrderBook:\n{exchange.GetSortedOrderBook("BTCUSDT", 10)}')
    #logger.info(f'GETBestPQOrderBook:\n{exchange.GETBestPQOrderBook("BTCUSDT")}')
    #logger.info(f'GetLotFilte:\n{exchange.GetLotFilte(symbol)}')
    #logger.info(f'GetPriceFilter:\n{exchange.GetPriceFilter(symbol)}')
    #logger.info(f'GetMinNotional:\n{exchange.GetMinNotional("BTCUSDT")}')
    #print(exchange.exportKlines(symbol, "4h", 7482))
    print(exchange.exportKlines(symbol, "4h",init_time=1577836800000, end_time=1685588400000))
    exit()



if __name__ == '__main__':
    Main()
