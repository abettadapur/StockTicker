from stocks import db
import datetime, time

class Stock(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(10), unique=True)
	reports = db.relationship("StockReport", backref="stock")
	
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
		return '<StockReport %r>' % self.symbol
		
	def as_dict(self):
		dict_repr = {c.name: getattr(self, c.name) for c in self.__table__.columns}
		dict_repr['timestamp'] = time.mktime(dict_repr['timestamp'].timetuple())
		dict_repr['stock'] = self.stock.as_dict()
		return dict_repr

	

