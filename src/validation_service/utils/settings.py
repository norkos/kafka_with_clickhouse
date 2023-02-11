import os

ENCODING = 'utf-8'

KAFKA_URL = os.environ.get('KAFKA_URL', '')
CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL', '')
PORT = int(os.environ.get('PORT', '8080'))
DEBUG_LOGGER_LEVEL = (os.environ.get('DEBUG_LOGGER_LEVEL', 'True') == 'True')
