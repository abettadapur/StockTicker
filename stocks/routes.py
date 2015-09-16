from stocks import db
from stocks.rest import api as stock_api
from stocks import app
from flask import render_template
from flask_restful import Api

api = Api(app)
api.add_resource(stock_api.HelloWorld, '/api')
api.add_resource(stock_api.ListStockResource, '/api/stocks')

@app.route('/')
def index():
	return render_template("index.html")