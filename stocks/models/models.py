from stocks import db

class Stock(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(10), unique=True)
	
	def __init__(self, symbol):
		self.symbol = symbol
	
	def __repr__(self):
		return '<Stock %r>' % self.symbol
		
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

