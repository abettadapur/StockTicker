from flask_restful import Resource
from stocks.models.models import Stock, StockReport

class HelloWorld(Resource):
	def get(self):
		return {"hello": "world"}


class ListStockResource(Resource):
	def get(self):
		return [c.as_dict() for c in Stock.query.all()]
		
class StockReportResource(Resource):
	
	def get(self, symbol):
		print symbol
		stock_report = StockReport.query.join(Stock).filter(Stock.symbol==symbol)
		stock_reports = [c.as_dict() for c in stock_report]
		return stock_reports
	
class FilteredStockReportResource(Resource):
	
	def get(self):
		filtered_stocks = StockReport.query.filter(StockReport.stock_float is not None).filter(StockReport.stock_float<300000000).filter(StockReport.quarterly_growth > 25.0).filter(StockReport.one_week > 10.0).filter(StockReport.one_month > 15.0).filter(StockReport.three_month > 25.0)
		return [c.as_dict() for c in filtered_stocks]
		
	