from stocks import app
from stocks.etc import config
import logging

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, filename="logs/server.log")
	logger = logging.getLogger(__name__)
	handler = logging.StreamHandler()
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger = logging.getLogger("werkzeug")
	logger.addHandler(handler)
	logger.info("Starting server")
	app.run(config.BIND, config.PORT, debug=True)