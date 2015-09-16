from stocks.models.models import Stock, StockReport
from stocks.finance.api import FinanceApi
from stocks import db

if __name__ == "__main__":
	api = FinanceApi()
	stocks = api.get_symbols()
	 
	#Add stocks to database
	
	for stock in stocks:
		queried_stock = db.session.query(Stock).filter_by(symbol=stock.symbol).first()
		if not queried_stock:
			db.session.add(stock)
		
	db.session.commit()	
	
	stocks = db.session.query(Stock).all()
	for stock in stocks:
		stock_report = api.get_stock_information(stock)
		db.session.add(stock_report)
	
	db.session.ccommit()

