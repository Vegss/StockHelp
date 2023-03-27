import yfinance as yf

class Stock:
    def __init__(self, ticker, period=None, startDate=None, endDate=None, interval="1d"):
        try:
            self.ticker = ticker
            self.data = yf.Ticker(self.ticker)
            self.info = self.data.info
            self.name = self.info["shortName"]
            self.historicData = self.get_historic_data(period, startDate, endDate, interval)
        except AttributeError:
            return None
    
    def get_historic_data(self, period, startDate, endDate, interval):
        if startDate and endDate:
            return yf.Ticker(self.ticker).history(start=startDate, end=endDate, interval=interval)
        elif period:
            return yf.Ticker(self.ticker).history(period=period, interval=interval)
        return yf.Ticker(self.ticker).history(period="max", interval=interval)
    


if __name__ == "__main__":
    startDate = "2019-01-01"
    endDate = "2020-01-01"
    stock = Stock("AAPL", startDate=startDate, endDate=endDate).data.tz_localize(None)
    stock.index = stock.index.strftime("%Y-%m-%d")
    stock.to_excel("test.xlsx")