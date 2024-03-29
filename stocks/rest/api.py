﻿from stocks import db
from flask_restful import Resource, reqparse, abort
from stocks.models.models import Stock, StockReport, StockDetail, Setting, Email
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
        setting = Setting.query.all()[0]
        stock_float = args['float'] if args['float'] is not None else setting.float_threshold
        yoy_growth = args['yoy_growth'] if args['yoy_growth'] is not None else setting.quarterly_growth_threshold
        onew_growth = args['onew_growth'] if args['onew_growth'] is not None else setting.one_week_threshold
        onem_growth = args['onem_growth'] if args['onem_growth'] is not None else setting.one_month_threshold
        threem_growth = args['threem_growth'] if args['threem_growth'] is not None else setting.three_month_threshold

        max_date = db.session.query(db.func.max(StockReport.timestamp)).scalar()
        filtered_stocks =  StockReport.query \
        .filter(StockReport.stock_float is not None) \
        .filter(StockReport.stock_float < stock_float) \
        .filter(StockReport.quarterly_growth > yoy_growth) \
        .filter(StockReport.one_week > onew_growth) \
        .filter(StockReport.one_month > onem_growth) \
        .filter(StockReport.three_month > threem_growth) \
        .filter(StockReport.timestamp == max_date) \
        .all()
        
        stocks_dict = {}
        for stock in filtered_stocks:
            if stock.stock.symbol not in stocks_dict:
                stocks_dict[stock.stock.symbol] = stock
        return [c.as_dict() for c in stocks_dict.values()]

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
        
        self.reqparse.add_argument('one_week_threshold', type=str, required=True, location='json',
                                   help='Need a display name for the setting')
        self.reqparse.add_argument('one_month_threshold', type=str, required=True, location='json',
                                   help='Need a display name for the setting')
        self.reqparse.add_argument('three_month_threshold', type=str, required=True, location='json',
                                   help='Need a display name for the setting')
        self.reqparse.add_argument('quarterly_growth_threshold', type=str, required=True, location='json',
                                   help='Need a display name for the setting')
        self.reqparse.add_argument('float_threshold', type=str, required=True, location='json',
                                    help='Need a display name for the setting')                                                                      
                                   
        super(SettingsResource, self).__init__()

    def get(self):
        return (Setting.query.all()[0]).as_dict()

    def post(self):
        args = self.reqparse.parse_args()
        
        setting = Setting.query.all()[0]
        setting.one_week_threshold = args['one_week_threshold']
        setting.one_month_threshold = args['one_month_threshold']
        setting.three_month_threshold = args['three_month_threshold']
        setting.quarterly_growth_threshold = args['quarterly_growth_threshold']
        setting.float_threshold = args['float_threshold']
        
        db.session.commit()
       
class EmailResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json', help='Need email address in POST')
        
        self.update_reqparse = reqparse.RequestParser()
        self.update_reqparse.add_argument('email', type=str, required=True, location='json', help='Need email address in PUT')
        self.update_reqparse.add_argument('old_email', type=str, required=True, location='json', help='Need old email address in PUT')
        
        super(EmailResource, self).__init__()
    
    
    def get(self):
        emails = Email.query.all()
        return [e.as_dict() for e in emails]
        
    def post(self):
        args = self.reqparse.parse_args()
        email_str = args['email']
        
        if Email.query.filter(Email.email == email_str).scalar():
            return "This email already exists in the database", 400
        
        email = Email(email_str)
        db.session.add(email)
        db.session.commit()
        
        return "Added", 200
 
class DeleteEmailResource(Resource):
    def __init__(self):
        super(DeleteEmailResource, self).__init__()
        
    def delete(self, email):
        print email
        email_record = Email.query.filter(Email.email == email).scalar()
        if email_record:
            db.session.delete(email_record)
            db.session.commit()
            
       
       
     
        
        
