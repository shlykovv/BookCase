import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f'{__name__}.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
))

logger.addHandler(file_handler)
