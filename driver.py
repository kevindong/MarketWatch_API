from MarketWatch import *
import os

email = ''
password = ''

try:
	email = os.environ['MARKETWATCH_EMAIL']
	password = os.environ['MARKETWATCH_PASSWORD']
	print('Your credentials have been successfully read from your env variables.')
except KeyError:
	print('You have not set your MarketWatch credentials in your env variables.\n'
		+ 'Please input your credentials for this session now.')
	email = input('Email: ')
	password = input('Password: ')
	print('Your credentials have been successfully saved for just this session.')

api = MarketWatch()

api.buy("SNAP", 1)
api.buy("SNAP", 1, Term.DAY)
api.buy("SNAP", 1, Term.INDEFINITE, PriceType.LIMIT, 1)