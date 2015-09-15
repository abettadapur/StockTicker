from stocks.models.models import Stock, StockReport
from stocks.finance.api import FinanceApi

if __name__ == "__main__":
	api = FinanceApi()
	stocks = api.get_symbols()
	print stocks

