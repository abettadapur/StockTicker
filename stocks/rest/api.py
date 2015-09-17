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
		
	