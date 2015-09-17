from stocks.models.models import Stock, StockReport
from stocks.finance.api import FinanceApi
from stocks import db
from stocks import mail

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
                print "Processing %s" % stock.symbol
		stock_report = api.get_stock_information(stock)
		db.session.add(stock_report)
		db.session.commit()
		
	filtered_stocks = StockReport.query.filter(StockReport.stock_float is not None).filter(StockReport.stock_float<300000000).filter(StockReport.quarterly_growth > 25.0).filter(StockReport.one_week > 10.0).filter(StockReport.one_month > 15.0).filter(StockReport.three_month > 25.0)
	mail.send_mail(filtered_stocks)
	
                
	
	

