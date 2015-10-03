from flask import Flask, render_template
from flask_restful import Api
import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.triangle import Triangle


app = Flask(__name__)
Triangle(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/temp.db'

db = SQLAlchemy(app)

import stocks.routes