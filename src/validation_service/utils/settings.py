import os

ENCODING = 'utf-8'

KAFKA_URL = os.environ.get('KAFKA_URL', '')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', '')
PORT = int(os.environ.get('PORT', '8080'))
DEBUG_LOGGER_LEVEL = (os.environ.get('DEBUG_LOGGER_LEVEL', 'True') == 'True')
