from stocks.finance.api import FinanceApi
from stocks.models.models import Stock

api = FinanceApi()
report  =  api.get_stock_information(Stock("AAPL"))
print report.one_month