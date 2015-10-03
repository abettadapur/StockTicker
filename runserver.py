from stocks import app
from stocks.etc import config
import logging

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)
	logger.info("Starting server")
	app.run(config.BIND, config.PORT, debug=True)