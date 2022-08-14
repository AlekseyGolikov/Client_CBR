# from os import path, remove
import logging
import client

FILE_NAME = 'logs/{}.log'.format(client.__name__)
# if path.isfile('logs/{}.log'.format(client.__name__)):
#     remove('logs/{}.log'.format(client.__name__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger_file_handler = logging.FileHandler(FILE_NAME, mode='a')
logger_file_handler.setLevel(logging.INFO)

logger_stream_handler = logging.StreamHandler()
logger_stream_handler.setLevel(logging.INFO)

logger_formatter = logging.Formatter('%(name)s - %(filename)s - %(asctime)s - %(levelname)s - %(message)s')

logger_file_handler.setFormatter(logger_formatter)
logger_stream_handler.setFormatter(logger_formatter)

logger.addHandler(logger_file_handler)
logger.addHandler(logger_stream_handler)
logger.info('Настройка логгирования окончена!')