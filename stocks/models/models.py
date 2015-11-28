from stocks import db
import datetime, time


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True)
    exchange = db.Column(db.String(50))
    industry = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    reports = db.relationship("StockReport", backref="stock")
    detailed_reports = db.relationship("StockDetail", backref="stock")

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return '<Stock %r>' % self.symbol

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class StockReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    closing_price = db.Column(db.Float)
    stock_float = db.Column(db.Float)
    quarterly_growth = db.Column(db.Float)
    one_week = db.Column(db.Float)
    one_month = db.Column(db.Float)
    three_month = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    def __init__(self, stock, timestamp):
        self.stock_id = stock.id
        self.timestamp = timestamp

    def __repr__(self):
        return '<StockReport %r>' % self.id

    def as_dict(self):
        dict_repr = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dict_repr['timestamp'] = time.mktime(dict_repr['timestamp'].timetuple())
        dict_repr['stock'] = self.stock.as_dict()
        return dict_repr
    
    @staticmethod   
    def get_filtered_reports():
        max_date = db.session.query(db.func.max(StockReport.timestamp)).scalar()
        return StockReport.query \
        .filter(StockReport.stock_float is not None) \
        .filter(StockReport.stock_float < 300000000) \
        .filter(StockReport.quarterly_growth > 25.0) \
        .filter(StockReport.one_week > 10.0) \
        .filter(StockReport.one_month > 15.0) \
        .filter(StockReport.three_month > 25.0) \
        .filter(StockReport.timestamp == max_date) \
        .all()

class StockDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    price = db.Column(db.Float)
    change = db.Column(db.Float)
    volume = db.Column(db.Float)
    open = db.Column(db.Float)
    days_high = db.Column(db.Float)
    days_low = db.Column(db.Float)
    year_high = db.Column(db.Float)
    year_low = db.Column(db.Float)
    fifty_avg = db.Column(db.Float)
    twohundred_avg = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    def __init__(self, stock, timestamp):
        self.stock_id = stock.id
        self.timestamp = timestamp

    def __repr__(self):
        return '<StockReport %r>' % self.id

    def as_dict(self):
        dict_repr = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dict_repr['timestamp'] = time.mktime(dict_repr['timestamp'].timetuple())
        dict_repr['stock'] = self.stock.as_dict()
        return dict_repr

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    one_week_threshold = db.Column(db.Float)
    one_month_threshold = db.Column(db.Float)
    three_month_threshold = db.Column(db.Float)
    quarterly_growth_threshold = db.Column(db.Float)
    float_threshold = db.Column(db.Float)

    def __init__(self):
       pass

    def __repr__(self):
        return '<Setting %r>' % self.id

    def as_dict(self):
        dict_repr = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return dict_repr
        
class Email(db.Model):
    email = db.Column(db.String(150), unique=True, primary_key=True)
    
    def __init__(self, email):
        self.email = email
    
    def __repr__(self):
        return '<Email %s>' % self.email
    
    def as_dict(self):
        return self.email
