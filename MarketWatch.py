'''
NOT READY FOR USAGE: DO NOT USE

TODO list for API:
- Check to make sure the user has the enough cash/security on hand to
  execute the order
- Implement function to get status of order
- Implement function to get all pending orders
- Implement function to cancel pending order
- Implement function to cancel all pending orders
- Write unit/integration tests?
- Implement function to get all held securities
- Implement function to get buying power
- Implement function to get available cash
'''

import json
import requests
from enum import Enum
from lxml import html

class Term(Enum):
	DAY = 'DayOrder'
	INDEFINITE = 'Cancelled'

class PriceType(Enum):
	MARKET = 1
	LIMIT = 2
	STOP = 3

class OrderType(Enum):
	BUY = 'Buy'
	SELL = 'Sell'
	SHORT = 'Short'
	COVER = 'Cover'

class MarketWatch:
	def __init__(self, email, password, game, debug = False):
		self.debug = debug
		self.game = game
		self.session = requests.Session()
		url = 'http://id.marketwatch.com/auth/submitlogin.json'
		headers = {'Content-Type': 'application/json'}
		data = {
			'username': email,
			'password': password,
			'savelogin': 'true',
		}
		response = self.session.post(url=url, headers=headers, json=data)
		response = json.loads(response.text)
		print('Login:', response['result'])
		try:
			self.session.get(url=response['url'])
		except KeyError:
			print('Login failed.')
			exit(1)

	def getPrice(self, ticker):
		try:
			page = requests.get("http://www.marketwatch.com/investing/stock/%s" % ticker)
			tree = html.fromstring(page.content)
			price = tree.xpath("/html/body/div[1]/div[3]/div[2]/div/div/div[2]/h3/bg-quote/text()")
			return round(float(price[0]), 2)
		except:
			return None

	def buy(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user has enough money
		return self.orderDriver(ticker, shares, term, priceType, price, OrderType.BUY)

	def short(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user has enough money
		return self.orderDriver(ticker, shares, term, priceType, price, OrderType.SHORT)

	def sell(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user actually owns the shares
		return self.orderDriver(ticker, shares, term, priceType, price, OrderType.SELL)

	def cover(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user actually has a short position
		return self.orderDriver(ticker, shares, term, priceType, price, OrderType.COVER)

	def orderDriver(self, ticker, shares, term, priceType, price, orderType):
		ticker = self.validateTicker(ticker)
		payload = [{"Fuid": ticker, "Shares": str(shares), "Type": orderType.value, "Term": term.value}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = str(price)
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = str(price)
		return self.submit(payload)

	def validateTicker(self, ticker):
		page = self.session.post('http://www.marketwatch.com/game/' + self.game + '/trade?week=1', data={'search': ticker, 'partial': 'true', 'view': 'grid'})
		tree = html.fromstring(page.content)

		try:
			tickerSymbol = tree.xpath('//div/div[3]/div/@data-symbol')[0]
		except:
			return None

		if (tree.xpath('//div/div[3]/div/@class')[0] == 'chip disabled'):
			return None
		else:
			return tickerSymbol

	def submit(self, payload):
		if (self.debug):
			print(payload)
			return payload
		else:
			url = ('http://www.marketwatch.com/game/%s/trade/submitorder' % self.game)
			headers = {'Content-Type': 'application/json'}
			response = json.loads((self.session.post(url=url, headers=headers, json=payload)).text)
			return(response)
