import os

CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL', '')
PORT = int(os.environ.get('PORT', '8080'))
DEBUG_LOGGER_LEVEL = (os.environ.get('DEBUG_LOGGER_LEVEL', 'True') == 'True')
