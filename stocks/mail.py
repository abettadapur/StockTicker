import smtplib
from stocks.models.models import Stock, StockReport
import json
import datetime
  
gmail_user = "alexbettadapur@gmail.com"
gmail_pwd = "dhypzgwzzdhxtyzk"
fromaddr = 'alexbettadapur@gmail.com'
toaddr = ['alexbettadapur@gmail.com']  #must be a list
subject = 'Stock Report for {date}'
message = """\From: {fromaddr}\nTo: {toaddr}\nSubject: {subj}\n\n{msg}
		"""
def send_mail(stock_reports):
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(fromaddr, toaddr, 
			message.format(
				fromaddr=fromaddr, 
				toaddr=", ".join(toaddr) ,
				subj=subject.format(datetime.datetime.now().strftime("%Y-%m-%d")), 
				msg=json.dumps([c.as_dict() for c in stock_reports])
			)
		)
		server.close()
	except Exception as ex:
		print ex	
