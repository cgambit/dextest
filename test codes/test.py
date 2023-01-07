sender1_a='asdf34134'
sender1_pk='carlg'

sender2_a='oioiyhj234'
sender2_pk='gonyot'

sender3_a='iyhlkn123'
sender3_pk='chessmining'

sender_creds = [('asdf34134', 'carlg'), ('oioiyhj234', 'gonyot')]

def sender_cred1(address, pk):
    print('sender1 address :', address)
    print('sender1 pk :', pk)

def sender_cred2(address, pk):
    print('sender2 address :', address)
    print('sender2 pk :', pk)

for i, cred in enumerate(sender_creds):
  if i == 0:
    sender_cred1(cred[0], cred[1])
  elif i == 1:
    sender_cred2(cred[0], cred[1])


import logging
import csv

# Set up the logger
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

# Create a file handler to write the logs to a CSV file
file_handler = logging.FileHandler('logs.csv')
formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Log some messages
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')

# Close the file handler
file_handler.close()



# Here is an example of how you can create a logger in Python and save the logs to a CSV file
import logging
import csv

# create logger with 'spam_application'
logger = logging.getLogger('logger_name')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('log.csv')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# example log messages
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

# To use this logger in your main.py file, you can import the logger and use it to log messages. For example:

import logger

logger.debug('This is a debug message')
logger.info('This is an info message')