'''
MarketWatch API
April 17, 2017

Probably ready for use.
'''

from MarketWatch import *
import os

def printOrder(order):
	print("Order: %d" % order.id)
	print("Ticker: %s" % order.ticker)
	print("Quantity: %d" % order.quantity)
	print("Order Type: %s" % order.orderType)
	print("Price Type: %s" % order.priceType)
	if (order.price != None):
		print("Price: $%.2f" % order.price)
	print("\n")

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

'''
api.cancelAllOrders()
orders = api.getOrders()

for item in orders:
	printOrder(item)

print(api.validateTicker("APPL"))
print(api.validateTicker("APPLKLJDZF"))
print(api.validateTicker("AAPL"))
print(api.validateTicker("JNUG"))
print(api.validateTicker("SNAP"))
print(api.validateTicker("GOOG"))

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