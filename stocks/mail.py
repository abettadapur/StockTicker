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
	
	rows = []

	for report in stock_reports:
	
		report_dict = report.as_dict()
		stock_dict = report_dict["stock"]
		
		symbol = stock_dict["symbol"]
		if symbol == None:
			continue
		
		price = report_dict["closing_price"]
		if price == None:
			price = ""
		else:
			price = '$' + str(report_dict["closing_price"])
		
		stock_float = report_dict["stock_float"]
		if stock_float == None:
			stock_float = ""
		else:
			stock_float = str(int(report_dict["stock_float"]))
			
		growth = report_dict["quarterly_growth"]
		if growth == None:
			growth = ""
		else:
			growth = str(report_dict["quarterly_growth"]) + '%'
		
		one_week = report_dict["one_week"]
		if one_week == None:
			one_week = ""
		else:
			one_week = str('%.2f'%(report_dict["one_week"]*10)) + '%'
			
		one_month = report_dict["one_month"]
		if one_month == None:
			one_month = ""
		else:
			one_month = str('%.2f'%(report_dict["one_month"]*10)) + '%'
			
		three_month = report_dict["three_month"]
		if three_month == None:
			three_month = ""
		else:
			three_month = str('%.2f'%(report_dict["three_month"]*10)) + '%'
		
		row = ""
		
		row += symbol
		row += "</font></TD>"
		
		row += "<TD align=\"right\"><font face=\"verdana\">"
		row += price
		row += "</font></TD>"
		
		row += "<TD align=\"right\"><font face=\"verdana\">"
		row += stock_float
		row += "</font></TD>"
		
		row += "<TD align=\"right\"><font face=\"verdana\">"
		row += growth
		row += "</font></TD>"
		
		row += "<TD align=\"right\"><font face=\"verdana\">"
		row += one_week
		row += "</font></TD>"
		
		row += "<TD align=\"right\"><font face=\"verdana\">"
		row += one_month
		row += "</font></TD>"
		
		row += "<TD align=\"right\"><font face=\"verdana\">"
		row += three_month
		row += "</font></TD>"
		
		row += "</TR>"
		
		rows.append(row)
		
	rows.sort()
	
	current_color = "deepskyblue"
	
	for row in rows:
		if current_color == "deepskyblue":
			current_color = "white"
		elif current_color == "white":
			current_color = "deepskyblue"
	
		row = "<TR style=\"background-color:" + current_color + ";font-size:13px\"><TD><font face=\"verdana\">" + row
		htmlcode += row
		

	htmlcode += "</TABLE>"
	
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