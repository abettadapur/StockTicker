import requests
import requests_ftp
import csv
import StringIO
import time
import re
from bs4 import BeautifulSoup

class FinanceApi(object):
	
	def __init__(self):
		self.scrape_url = "http://finance.yahoo.com/q/ks?s={symbol}"
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
			symbols.append(str(row[0]))
	
		symbols.pop(0)
		symbols.pop(len(symbols)-1)
	
		symbols_file = s.retr(self.otherlisted_url).content
		f = StringIO.StringIO(symbols_file)
		reader = csv.reader(f, delimiter='|')
	
		for row in reader:
			if str(row[2]) == "N":
				symbols.append(str(row[0]))
	
		return symbols
		
	def get_stock_information(self, symbol):
		html = requests.get(self.scrape_url.format(symbol=symbol)).content
		soup = BeautifulSoup(html, 'lxml')
		
		for elem in soup(text="Float:"):
			print elem.parent
			print elem.parent.next_sibling
			
		for elem in soup(text="Qtrly Revenue Growth (yoy):"):
			print elem.parent
			print elem.parent.next_sibling
			


if __name__ == "__main__":
	api = FinanceApi()
	api.get_stock_information("AAPL")
	# symbols = get_symbols()
	
	# start_time = time.time()

	# for i in range(0, 100):
	# 	share = Share(symbols[i])
	# 	print("{0}: Open:{1} , Price: {2}".format(symbols[i], str(share.get_open()), str(share.get_price())))

	# print("100 shares in {0} seconds".format(str(time.time() - start_time)))
