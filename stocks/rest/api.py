from flask_restful import Resource, reqparse
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
	
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('float', type=str, required=False, location='args', help='No token to verify')
		self.reqparse.add_argument('yoy_growth', type=str, required=False, location='args', help='No token to verify')
		self.reqparse.add_argument('onew_growth', type=str, required=False, location='args', help='No token to verify')
		self.reqparse.add_argument('onem_growth', type=str, required=False, location='args', help='No token to verify')
		self.reqparse.add_argument('threem_growth', type=str, required=False, location='args', help='No token to verify')
		super(FilteredStockReportResource, self).__init__()

	
	def get(self):
		args = self.reqparse.parse_args()
		stock_float = args['float'] if args['float'] is not None else 300000000
		yoy_growth = args['yoy_growth'] if args['yoy_growth'] is not None else 25.0
		onew_growth = args['onew_growth'] if args['onew_growth'] is not None else 10.0
		onem_growth = args['onem_growth'] if args['onem_growth'] is not None else 15.0
		threem_growth = args['threem_growth'] if args['threem_growth'] is not None else 25.0
		
		print('float' in args)
		print(stock_float)
		
		filtered_stocks = StockReport.query.filter(StockReport.stock_float is not None).filter(StockReport.stock_float<stock_float).filter(StockReport.quarterly_growth > yoy_growth).filter(StockReport.one_week > onew_growth).filter(StockReport.one_month > onem_growth).filter(StockReport.three_month > threem_growth)
		return [c.as_dict() for c in filtered_stocks]
		
	