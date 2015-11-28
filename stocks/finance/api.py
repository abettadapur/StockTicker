import requests
import requests_ftp
import csv
import StringIO
import time
import re
from datetime import datetime, date, time
from stocks.etc.util import convert_price_string
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from stocks.models.models import Stock, StockReport, StockDetail
from yahoo_finance import Share


class FinanceApi(object):
    def __init__(self):
        self.scrape_url = "http://finance.yahoo.com/q/ks?s={symbol}"
        self.historical_url = "http://ichart.yahoo.com/table.csv?s={symbol}&a={from_month}&b={from_date}&c={from_year}&d={to_month}&e={to_date}&f={to_year}&g=d&ignore=.csv"
        self.nasdaqlisted_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
        self.otherlisted_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt"
        self.index_url = "http://money.cnn.com/data/markets/"

    def get_symbols(self):

        requests_ftp.monkeypatch_session()
        s = requests.Session()

        symbols_file = s.retr(self.nasdaqlisted_url).content
        f = StringIO.StringIO(symbols_file)
        reader = csv.reader(f, delimiter='|')
        symbols = []

        for row in reader:
            symbols.append(Stock(str(row[0])))

        symbols.pop(0)
        symbols.pop(len(symbols) - 1)

        symbols_file = s.retr(self.otherlisted_url).content
        f = StringIO.StringIO(symbols_file)
        reader = csv.reader(f, delimiter='|')

        for row in reader:
            if str(row[2]) == "N":
                symbols.append(Stock(str(row[0])))

        return symbols

    def fill_stock_metadata(self, stock):
        share = Share(stock.symbol)
        stock.exchange = share.get_stock_exchange();
        metadata = share.get_info()
        stock.industry = metadata["Industry"] if "Industry" in metadata else ""
        stock.sector = metadata["Sector"] if "Sector" in metadata else ""

    def get_detailed_stock_information(self, stock):
        share = Share(stock.symbol)
        stock_detail = StockDetail(stock, datetime.utcnow())

        stock_detail.price = share.get_price();
        stock_detail.change = share.get_change();
        stock_detail.volume = share.get_volume();
        stock_detail.open = share.get_open();
        stock_detail.days_high = share.get_days_high();
        stock_detail.days_low = share.get_days_low();
        stock_detail.year_high = share.get_year_high();
        stock_detail.year_low = share.get_year_low();
        stock_detail.fifty_avg = share.get_50day_moving_avg();
        stock_detail.twohundred_avg = share.get_200day_moving_avg();

        return stock_detail

    def get_stock_information(self, stock):
        
        stock_report = StockReport(stock, date.today())
        html = requests.get(self.scrape_url.format(symbol=stock.symbol)).content
        soup = BeautifulSoup(html, 'lxml')

        for elem in soup(text="Float:"):
            try:
                stock_report.stock_float = convert_price_string(elem.parent.next_sibling.string)
            except ValueError:
                stock_report.stock_float = None

        for elem in soup(text="Qtrly Revenue Growth (yoy):"):
            try:
                stock_report.quarterly_growth = float(elem.parent.next_sibling.string[:-1])
            except ValueError:
                stock_report.quarterly_growth = None

        self.get_historical_information(stock, stock_report)

        try:
            stock_report.closing_price = Share(stock.symbol).get_price()
        except:
            stock_report.closing_price = None

        return stock_report

    def get_historical_information(self, stock, stock_report):
        today = date.today().strftime("%Y-%m-%d")
        one_week = (date.today() - relativedelta(weeks=1)).strftime("%Y-%m-%d")
        one_month = (date.today() - relativedelta(months=1)).strftime("%Y-%m-%d")
        three_month = (date.today() - relativedelta(months=3)).strftime("%Y-%m-%d")

        share = Share(stock.symbol)
        
        one_week_history = share.get_historical(one_week, today)
        one_month_history = share.get_historical(one_month, today)
        three_month_history = share.get_historical(three_month, today)

        if len(one_week_history) > 0:
            stock_report.one_week = ((float(one_week_history[0]['Close']) - float(one_week_history[-1]['Open']))/float(one_week_history[-1]["Open"])) * 100.0
        else:
            stock_report.one_week = None;

        if len(one_month_history) > 0:
            stock_report.one_month = ((float(one_month_history[0]['Close']) - float(one_month_history[-1]['Open']))/float(one_month_history[-1]["Open"])) * 100.0
        else:
            stock_report.one_month = None;

        if len(three_month_history) > 0:
            stock_report.three_month = ((float(three_month_history[0]['Close']) - float(three_month_history[-1]['Open']))/float(three_month_history[-1]["Open"])) * 100.0
        else:
            stock_report.three_month = None;

    def get_historical_chart(self, stock, from_date, to_date):
        share = Share(stock.symbol)
        history = share.get_historical(from_date, to_date)
        return history

    def get_stock_indexes(self):
        html = requests.get(self.index_url).content
        soup = BeautifulSoup(html, 'lxml')
        stock_info_tag = soup.find("div", {"class": "markets-overview"})
        indexes = []
        for index in stock_info_tag.findAll("a", {"class": "ticker"}):
            name = index.find("span", {"class": "ticker-name"}).contents[0]
            points = index.find("span", {"class":"ticker-points"}).contents[0]
            points_change = index.find("span", {"class":"ticker-points-change"}).contents[0].contents[0]
            percentage_change = index.find("span", {"class":"ticker-name-change"}).contents[0].contents[0]
            indexes.append({"name": name, "price": points, "price_change": points_change, "percentage_change": percentage_change})

        return indexes


if __name__ == "__main__":
    api = FinanceApi()
    print(api.get_symbols())
    api.get_stock_information("AAPL")
    api.get_stock_information("MSFT")
# print api.get_symbols()
# api.get_historical_information("MSFT")
# symbols = get_symbols()

# start_time = time.time()

# for i in range(0, 100):
# 	share = Share(symbols[i])
# 	print("{0}: Open:{1} , Price: {2}".format(symbols[i], str(share.get_open()), str(share.get_price())))

# print("100 shares in {0} seconds".format(str(time.time() - start_time)))
