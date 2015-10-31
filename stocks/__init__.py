from flask import Flask, render_template
from flask_restful import Api
import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.triangle import Triangle
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger


app = Flask(__name__)
Triangle(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/temp.db'

db = SQLAlchemy(app)

import stocks.routes
from stocks import cronjob

scheduler = BackgroundScheduler(
	jobstores= {
		'default': SQLAlchemyJobStore(url='sqlite:///stocks/data/temp.db')
	},
	job_defaults={
		'max_instances': 1,
		'coalescing': True
	}
)
trigger = CronTrigger(day_of_week='mon-fri', hour=18, minute=0)
scheduler.add_job(cronjob.runjob, trigger=trigger, id='stocks', misfire_grace_time=43200, jobstore='default', replace_existing=True)
scheduler.start()

