'''
NOT READY FOR USAGE: DO NOT USE

TODO list for driver:
- Implement interactive CLI for using API
'''

from MarketWatch import *
import os

email = ''
password = ''
game = ''

try:
	email = os.environ['MARKETWATCH_EMAIL']
	password = os.environ['MARKETWATCH_PASSWORD']
	game = os.environ['MARKETWATCH_GAME']
	print('Your credentials have been successfully read from your env variables.')
except KeyError:
	print('You have not set your MarketWatch credentials in your env variables.\n'
		+ 'Please input your credentials for this session now.')
	email = input('Email: ')
	password = input('Password: ')
	game = input('Game: ')
	print('Your credentials have been successfully saved for just this session.')

api = MarketWatch(email, password, game, True)

orders = {
	"JNUG": 1,
	"IBM": 2,
	"SNAP": 3,
	"GOOG": 4
}

for i in orders:
	print(i + ': ' + str(orders[i]))
	response = api.cover(i, orders[i])
	if (response['succeeded']):
		print("Successfully submitted order.")
	else:
		print("Order failed.")
		print(response)

'''
api.buy("SNAP", 1)
api.sell("SNAP", 1)
api.short("SNAP", 1)
api.cover("SNAP", 1)
print("")
api.buy("SNAP", 1, Term.DAY)
api.sell("SNAP", 1, Term.DAY)
api.short("SNAP", 1, Term.DAY)
api.cover("SNAP", 1, Term.DAY)
print("")
api.buy("SNAP", 1, Term.INDEFINITE, PriceType.MARKET)
api.sell("SNAP", 1, Term.INDEFINITE, PriceType.MARKET)
api.short("SNAP", 1, Term.INDEFINITE, PriceType.MARKET)
api.cover("SNAP", 1, Term.INDEFINITE, PriceType.MARKET)
print("")
api.buy("SNAP", 1, Term.INDEFINITE, PriceType.LIMIT, 1)
api.sell("SNAP", 1, Term.INDEFINITE, PriceType.LIMIT, 1)
api.short("SNAP", 1, Term.INDEFINITE, PriceType.LIMIT, 1)
api.cover("SNAP", 1, Term.INDEFINITE, PriceType.LIMIT, 1)
print("")
api.buy("SNAP", 1, Term.INDEFINITE, PriceType.STOP, 1)
api.sell("SNAP", 1, Term.INDEFINITE, PriceType.STOP, 1)
api.short("SNAP", 1, Term.INDEFINITE, PriceType.STOP, 1)
api.cover("SNAP", 1, Term.INDEFINITE, PriceType.STOP, 1)
'''