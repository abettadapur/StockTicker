import threading
import logging
import time
import datetime
import multiprocessing
from stocks.models.models import Stock, StockReport
from stocks.finance.api import FinanceApi
from stocks import db
from stocks import mail


def process_stocks(thread_id, stocks):
    session = db.create_scoped_session()
    logging.basicConfig(level=logging.INFO, filename="logs/%s_job.log"%time.strftime('%m_%d_%Y'))
    logger = logging.getLogger("Thread %d"%thread_id)
    api = FinanceApi()
    total = len(stocks)
    counter = 0
    for stock in stocks:
        counter = counter + 1
        try:
            logger.info("%d stocks remain to be processed" % (total-counter))
            logger.info("Processing %s" % stock.symbol)
            stock_report = api.get_stock_information(stock)
            session.add(stock_report)
            session.commit()
        except Exception as ex:
            logger.error("Failed to process %s: %s" % (stock.symbol, ex)) 


def runjob():
    logging.basicConfig(level=logging.INFO, filename="logs/%s_job.log"%time.strftime('%m_%d_%Y'))
    logger = logging.getLogger("cronjob")
    logging.getLogger("requests").setLevel(logging.WARNING)
    api = FinanceApi()
    stocks = api.get_symbols()

    # Add stocks to database

    logger.info("Retrieving symbols and metadata")
    for stock in stocks:
        queried_stock = db.session.query(Stock).filter_by(symbol=stock.symbol).first()
        if not queried_stock:
            db.session.add(stock)
            
    db.session.commit()

    stocks = db.session.query(Stock).all()

    # threads = []
    # counter = 0
    # cores = multiprocessing.cpu_count()
    # print cores
    # for i in range(0, len(stocks), len(stocks)/cores):
    #     counter = counter + 1
    #     subset = stocks[i:i+len(stocks)/cores]
    #     threads.append(multiprocessing.Process(target=process_stocks, args=(counter, subset)))

    # for thread in threads:
    #     thread.start()
    
    # timeout = datetime.datetime.utcnow() + datetime.timedelta(hours=2, minutes=30)
    # while threading.active_count() > 2:
    #     print threading.active_count()
    #     if datetime.datetime.utcnow() > timeout:
    #         logger.error("TIMEOUT, terminating threads")
    #         for thread in threads:
    #             thread.terminate();
                
    #     time.sleep(5)


    logger.info("Sending emails")
    filtered_stocks = StockReport.get_filtered_reports()
    mail.send_mail(filtered_stocks)
    
def testjob():
    print("Ran Job")
