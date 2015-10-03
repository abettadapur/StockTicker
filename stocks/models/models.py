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
    display_name = db.Column(db.String(100))
    key = db.Column(db.String(30), unique=True)
    value = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(10))

    def __init__(self, name, key, value):
        self.display_name = name
        self.key = key
        self.value = value
        self.type = type(value).__name__

    def __repr__(self):
        return '<Setting %r>' % self.key

    def as_dict(self):
        dict_repr = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return dict_repr
