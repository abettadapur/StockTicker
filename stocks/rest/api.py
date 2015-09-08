from flask_restful import Resource
from stocks.models.models import Stock

class HelloWorld(Resource):
	def get(self):
		return {"hello": "world"}


class ListStockResource(Resource):
	def get(self):
		return [c.as_dict() for c in Stock.query.all()]
	