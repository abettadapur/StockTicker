import smtplib
from stocks.models.models import Stock, StockReport
  
gmail_user = "alexbettadapur@gmail.com"
gmail_pwd = "dhypzgwzzdhxtyzk"
fromaddr = 'alexbettadapur@gmail.com'
toaddr = ['abettadapur3@gatech.edu']  #must be a list
subject = 'Stock Report for {date}'

def send_mail(stock_reports):
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(fromaddr, toaddr, "Test")
		server.close()
	except:
		print "Failed to send message"
			
