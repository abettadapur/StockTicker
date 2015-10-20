#import smtplib
#from stocks.models.models import Stock, StockReport
#import json
#import datetime
  
#gmail_user = "alexbettadapur@gmail.com"
#gmail_pwd = "dhypzgwzzdhxtyzk"
#fromaddr = 'alexbettadapur@gmail.com'
#toaddr = ['alexbettadapur@gmail.com']  #must be a list
#subject = 'Stock Report for {date}'
#message = """\From: {fromaddr}\nTo: {toaddr}\nSubject: {subj}\n\n{msg}
#		"""
#def send_mail(stock_reports):
#	try:
#		server = smtplib.SMTP('smtp.gmail.com', 587)
#		server.ehlo()
#		server.starttls()
#		server.login(gmail_user, gmail_pwd)
#		server.sendmail(fromaddr, toaddr, 
#			message.format(
#				fromaddr=fromaddr, 
#				toaddr=", ".join(toaddr) ,
#				subj=subject.format(datetime.datetime.now().strftime("%Y-%m-%d")), 
#				msg=json.dumps([c.as_dict() for c in stock_reports])
#			)
#		)
#		server.close()
#	except Exception as ex:
#		print ex	

import requests
import datetime
from stocks.models.models import Stock, StockReport
from etc import config


def send_mail(stock_reports):

	#email_dot_html = open('email.html', 'w')

	htmlcode = "<TABLE cellpadding=\"4\"><caption><font face=\"verdana\" size=\"4\">This Week's Stocks</font></caption>"
	
	htmlcode += "<TR style=\"background-color:dodgerblue;font-size:14px\">"
	
	htmlcode += "<TH><font face=\"verdana\">Symbol</font></TH>"
	htmlcode += "<TH><font face=\"verdana\">Price</font></TH>"
	htmlcode += "<TH><font face=\"verdana\">Float</font></TH>"
	htmlcode += "<TH><font face=\"verdana\">Quarterly Growth</font></TH>"
	htmlcode += "<TH><font face=\"verdana\">Movement - 1 week</font></TH>"
	htmlcode += "<TH><font face=\"verdana\">Movement - 1 month</font></TH>"
	htmlcode += "<TH><font face=\"verdana\">Movement - 3 month</font></TH>"
	
	htmlcode += "</TR>"
	
	current_color = "deepskyblue"

	for report in stock_reports:
	
		if current_color == "deepskyblue":
			current_color = "white"
		elif current_color == "white":
			current_color = "deepskyblue"
	
		htmlcode += "<TR style=\"background-color:" + current_color + ";font-size:13px\">"
	
		report_dict = report.as_dict()
		stock_dict = report_dict["stock"]
		
		htmlcode += "<TD><font face=\"verdana\">"
		htmlcode += stock_dict["symbol"]
		htmlcode += "</font></TD>"
		
		htmlcode += "<TD><font face=\"verdana\">"
		htmlcode += '$' + str(report_dict["closing_price"])
		htmlcode += "</font></TD>"
		
		htmlcode += "<TD><font face=\"verdana\">"
		#htmlcode += str(int(report_dict["stock_float"]))
		htmlcode += str(report_dict["stock_float"])
		htmlcode += "</font></TD>"
		
		htmlcode += "<TD><font face=\"verdana\">"
		htmlcode += str(report_dict["quarterly_growth"]) + '%'
		htmlcode += "</font></TD>"
		
		htmlcode += "<TD><font face=\"verdana\">"
		#htmlcode += str('%.2f'%(report_dict["one_week"])) + '%'
		htmlcode += str(report_dict["one_week"]) + '%'
		htmlcode += "</font></TD>"
		
		htmlcode += "<TD><font face=\"verdana\">"
		#htmlcode += str('%.2f'%(report_dict["one_month"])) + '%'
		htmlcode += str(report_dict["one_month"]) + '%'
		htmlcode += "</font></TD>"
		
		htmlcode += "<TD><font face=\"verdana\">"
		#htmlcode += str('%.2f'%(report_dict["three_month"])) + '%'
		htmlcode += str(report_dict["three_month"]) + '%'
		htmlcode += "</font></TD>"
		
		htmlcode += "</TR>"

	htmlcode += "</TABLE>"
	
	print htmlcode
	
	#email_dot_html.write(htmlcode)

	try:
		requests.post(
			"https://api.mailgun.net/v3/bettadapur.com/messages",
			auth=("api", config.MAILGUN_KEY),
			data={
				"from": "{0} <{1}@bettadapur.com>".format(config.FROM_NAME, config.FROM_ADDR),
				"to": ["kendallmerritt@gmail.com"],
				"subject": config.SUBJECT.format(datetime.date.today()),
				"text": "",
				"html": htmlcode
			})

	except Exception as ex:
		print "SEND MAIL EXCEPTION"
		print ex
		#pass