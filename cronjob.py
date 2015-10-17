import threading
import logging
import time
import multiprocessing
from stocks.models.models import Stock, StockReport
from stocks.finance.api import FinanceApi
from stocks import db
from stocks import mail


def process_stocks(thread_id, stocks):
    session = db.create_scoped_session()
    logger = logging.getLogger("Thread %d"%thread_id)
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
            logger.error("Failed to process %s" % stock.symbol)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
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

    threads = []
    counter = 0
    cores = multiprocessing.cpu_count()
    for i in range(0, len(stocks), len(stocks)/cores):
        counter = counter + 1
        subset = stocks[i:i+len(stocks)/cores]
        threads.append(threading.Thread(target=process_stocks, args=(counter, subset)))

    for thread in threads:
        thread.daemon = True
        thread.start()

    while threading.active_count() > 1:
        print threading.active_count()
        time.sleep(5)



    filtered_stocks = StockReport.query.filter(StockReport.stock_float is not None).filter(
        StockReport.stock_float < 300000000).filter(StockReport.quarterly_growth > 25.0).filter(
        StockReport.one_week > 0.10).filter(StockReport.one_month > 0.15).filter(StockReport.three_month > 0.25)
    mail.send_mail(filtered_stocks)
