from stocks import db
from flask_restful import Resource, reqparse, abort
from stocks.models.models import Stock, StockReport, StockDetail, Setting
from stocks.finance.api import FinanceApi
import datetime


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


class ListStockResource(Resource):
    def get(self):
        return [c.as_dict() for c in Stock.query.all()]


class StockReportResource(Resource):
    def get(self, symbol):
        print symbol
        stock_report = StockReport.query.join(Stock).filter(Stock.symbol == symbol)
        stock_reports = [c.as_dict() for c in stock_report]
        return stock_reports


class FilteredStockReportResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('float', type=str, required=False, location='args', help='No token to verify')
        self.reqparse.add_argument('yoy_growth', type=str, required=False, location='args', help='No token to verify')
        self.reqparse.add_argument('onew_growth', type=str, required=False, location='args', help='No token to verify')
        self.reqparse.add_argument('onem_growth', type=str, required=False, location='args', help='No token to verify')
        self.reqparse.add_argument('threem_growth', type=str, required=False, location='args',
                                   help='No token to verify')
        super(FilteredStockReportResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        stock_float = args['float'] if args['float'] is not None else 300000000
        yoy_growth = args['yoy_growth'] if args['yoy_growth'] is not None else 25.0
        onew_growth = args['onew_growth'] if args['onew_growth'] is not None else 10.0
        onem_growth = args['onem_growth'] if args['onem_growth'] is not None else 15.0
        threem_growth = args['threem_growth'] if args['threem_growth'] is not None else 25.0

        filtered_stocks = StockReport.query.filter(StockReport.stock_float is not None).filter(
            StockReport.stock_float < stock_float).filter(StockReport.quarterly_growth > yoy_growth).filter(
            StockReport.one_week > onew_growth).filter(StockReport.one_month > onem_growth).filter(
            StockReport.three_month > threem_growth).filter(
            StockReport.timestamp > datetime.datetime.utcnow() - datetime.timedelta(days=2))
        print [c.as_dict() for c in filtered_stocks]
        return [c.as_dict() for c in filtered_stocks]

class RealTimeStockResource(Resource):
    def get(self, symbol):
        stock = Stock.query.filter(Stock.symbol == symbol).first()
        if stock:
            stock_detail = StockDetail.query.join(Stock).filter(Stock.symbol == symbol).filter(
                StockDetail.timestamp > datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).first()
            if not stock_detail:
                finance_api = FinanceApi()
                stock_detail = finance_api.get_detailed_stock_information(stock)
                db.session.add(stock_detail)
                db.session.commit()
            return stock_detail.as_dict()

        else:
            abort(404, message='{"error": "%s was not found in the database"}' % symbol)


class HistoricalStockResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from', type=str, required=True, location='args', help='A from date is required')
        self.reqparse.add_argument('to', type=str, required=True, location='args', help='A to date is required')
        super(HistoricalStockResource, self).__init__()

    def get(self, symbol):
        args = self.reqparse.parse_args()

        # Note(abettadapur): This is a format check. pass the strings into the function anyway
        from_date = datetime.datetime.strptime(args['from'], "%Y-%m-%d")
        to_date = datetime.datetime.strptime(args['to'], "%Y-%m-%d")

        stock = Stock.query.filter(Stock.symbol == symbol).first()
        if stock:
            finance_api = FinanceApi()
            return finance_api.get_historical_chart(stock, args['from'], args['to'])
        else:
            abort(404, message='{"error": "%s was not found in the database"}' % symbol)


class IndexesResource(Resource):
    def get(self):
        finance_api = FinanceApi()
        return finance_api.get_stock_indexes()


class SettingsResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('key', type=str, required=False, location='args', help='No token to verify')

        self.create_reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, location='json',
                                   help='Need a display name for the setting')
        self.reqparse.add_argument('key', type=str, required=True, location='json',
                                   help='Need a display name for the setting')
        self.reqparse.add_argument('value', type=str, required=True, location='json',
                                   help='Need a display name for the setting')
        super(SettingsResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        key = args['key']

        if key is not None:
            settings = Setting.query.filter(Setting.key == key)
            if len(settings) == 0:
                abort(404, message='{"error": "No setting with this key was found"}')
            else:
                return [c.as_dict() for c in settings]

        else:
            return [c.as_dict() for c in Setting.query.all()]

    def post(self):
        pass
