import requests
import datetime
from stocks.models.models import Stock, StockReport
from etc import config
from jinja2 import Environment, PackageLoader

def send_mail(stock_reports):

	env = Environment(loader=PackageLoader('stocks', 'templates'))
	mailtemplate = env.get_template("mail.html")
	formatted_reports = []
	for report in stock_reports:
		report_dict = report.as_dict()
		
		symbol = report_dict["stock"]["symbol"]
		if symbol == None:
			continue
			
		if report_dict["closing_price"] == None:
			report_dict["closing_price"] = ""
		else:
			report_dict["closing_price"] = '$' + str(report_dict["closing_price"])
		
		if report_dict["stock_float"] == None:
			report_dict["stock_float"] = ""
		else:
			report_dict["stock_float"] = str(int(report_dict["stock_float"]))
			
		if report_dict["quarterly_growth"] == None:
			report_dict["quarterly_growth"] = ""
		else:
			report_dict["quarterly_growth"] = str(report_dict["quarterly_growth"]) + '%'
	
		if report_dict["one_week"] == None:
			report_dict["one_week"] = ""
		else:
			report_dict["one_week"] = str('%.2f'%(report_dict["one_week"]*10)) + '%'
			
		if report_dict["one_month"] == None:
			report_dict["one_month"] = ""
		else:
			report_dict["one_month"] = str('%.2f'%(report_dict["one_month"]*10)) + '%'
			
		if report_dict["three_month"] == None:
			report_dict["three_month"] = ""
		else:
			report_dict["three_month"] = str('%.2f'%(report_dict["three_month"]*10)) + '%'
		
		formatted_reports.append(report_dict)	
	
	
	htmlcode = mailtemplate.render(stocks=formatted_reports)
	try:
		requests.post(
			"https://api.mailgun.net/v3/bettadapur.com/messages",
			auth=("api", config.MAILGUN_KEY),
			data={
				"from": "{0} <{1}@bettadapur.com>".format(config.FROM_NAME, config.FROM_ADDR),
				"to": ["alexbettadapur@gmail.com"],
				"subject": config.SUBJECT.format(date = datetime.date.today()),
				"text": "",
				"html": htmlcode
			})

	except Exception as ex:
		print "SEND MAIL EXCEPTION"
		print ex
		#pass