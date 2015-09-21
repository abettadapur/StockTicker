import requests
import requests_ftp
import csv
import StringIO
import time
import re
from datetime import date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from stocks.models.models import Stock, StockReport
from yahoo_finance import Share

class FinanceApi(object):
	
	def __init__(self):
		self.scrape_url = "http://finance.yahoo.com/q/ks?s={symbol}"
		self.historical_url = "http://ichart.yahoo.com/table.csv?s={symbol}&a={from_month}&b={from_date}&c={from_year}&d={to_month}&e={to_date}&f={to_year}&g=d&ignore=.csv"
		self.nasdaqlisted_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
		self.otherlisted_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt"
			
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
		symbols.pop(len(symbols)-1)
	
		symbols_file = s.retr(self.otherlisted_url).content
		f = StringIO.StringIO(symbols_file)
		reader = csv.reader(f, delimiter='|')
	
		for row in reader:
			if str(row[2]) == "N":
				symbols.append(Stock(str(row[0])))
	
		return symbols
		
	def get_stock_information(self, stock):
		
		stock_report = StockReport(stock, date.today())
		html = requests.get(self.scrape_url.format(symbol=stock.symbol)).content
		soup = BeautifulSoup(html, 'lxml')
		
		for elem in soup(text="Float:"):
                        print elem.parent.next_sibling
                        try:
                                stock_report.stock_float = self.convert_price_string(elem.parent.next_sibling.string)
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
		one_week = date.today() - relativedelta(weeks=1)
		one_month = date.today() - relativedelta(months=1)
		three_month = date.today() - relativedelta(months=3)
		one_week_csv = requests.get(self.build_historical_url(stock.symbol, one_week, date.today()))
		one_month_csv = requests.get(self.build_historical_url(stock.symbol, one_month, date.today()))
		three_month_csv = requests.get(self.build_historical_url(stock.symbol, three_month, date.today()))
		
		def parse_csv(csv_file):
			f = StringIO.StringIO(csv_file)
			reader = csv.reader(f, delimiter=',')
			rows = []
			for row in reader:
				rows.append(row)	
			
			todays_price = rows[1]
			earliest_price = rows[-1]

			try:
				return (float(todays_price[4]) - float(earliest_price[1]))/float(earliest_price[1])
			except ValueError:
				return None
		
		if(one_week_csv.status_code==200):
				stock_report.one_week = float(parse_csv(one_week_csv.content))
		else:
				stock_report.one_week = None;
		if(one_month_csv.status_code==200):
				stock_report.one_month = float(parse_csv(one_month_csv.content))
		else:
				stock_report.one_month = None;
		if(three_month_csv.status_code==200):
				stock_report.three_month = float(parse_csv(three_month_csv.content))
		else:
				stock_report.three_month = None;
	
	def build_historical_url(self, symbol, from_date, to_date):
		url = self.historical_url.format(
			symbol=symbol,
			from_date=from_date.day,
			from_month = from_date.month-1,
			from_year = from_date.year,
			to_date = to_date.day,
			to_month = to_date.month-1,
			to_year = to_date.year,
		)
		return url
	
	def convert_price_string(self, price):
		lookup = {'K': 1000, 'M': 1000000, 'B': 1000000000}
		unit = price[-1]
                try:
                        number = float(price[:-1])
                        
                        if unit in lookup:
                                return lookup[unit] * number
                        
                        return int(price)
                
                except ValueError:
                        return -1
                        
	
if __name__ == "__main__":
	api = FinanceApi()
	print(api.get_symbols())
	api.get_stock_information("AAPL")
	api.get_stock_information("MSFT")
	#print api.get_symbols()
	#api.get_historical_information("MSFT")
	# symbols = get_symbols()
	
	# start_time = time.time()

	# for i in range(0, 100):
	# 	share = Share(symbols[i])
	# 	print("{0}: Open:{1} , Price: {2}".format(symbols[i], str(share.get_open()), str(share.get_price())))

	# print("100 shares in {0} seconds".format(str(time.time() - start_time)))
