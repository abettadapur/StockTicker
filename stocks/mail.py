import requests
import datetime
from stocks.models.models import Stock, StockReport
from etc import config


def send_mail(stock_reports):
    try:
        response = requests.post(
        "https://api.mailgun.net/v3/bettadapur.com/messages",
        auth=("api", config.MAILGUN_KEY),
        data={
	        "from": "{0} <{1}@bettadapur.com>".format(config.FROM_NAME, config.FROM_ADDR),
	        "to": ["alexbettadapur@gmail.com"],
	        "subject": config.SUBJECT.format(date=str(datetime.date.today())),
	        "text": "Test email"
        })
        print(response)

    except Exception as ex:
        print(ex.message)