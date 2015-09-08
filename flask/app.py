from flask import Flask, render_template
from flask_restful import Api
from rest import api as stock_api

app = Flask(__name__)
api = Api(app)

api.add_resource(stock_api.HelloWorld, '/api')

@app.route("/")
def index():
	return render_template('index.html')
	
if __name__ == "__main__":
	app.run('0.0.0.0', 5000, debug=True)