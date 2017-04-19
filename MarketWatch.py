'''
MarketWatch API
April 19, 2017
v1.0.0

Apache License 2.0
https://github.com/kevindong/marketwatch_api
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

class Order:
	def __init__(self, id, ticker, quantity, orderType, priceType, price = None):
		self.id = id
		self.ticker = ticker
		self.quantity = quantity
		self.orderType = orderType
		self.priceType = priceType
		self.price = price

class Position:
	def __init__(self, ticker, orderType, quantity):
		self.ticker = ticker
		self.orderType = orderType
		self.quantity = quantity

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
			page = self.session.get("http://www.marketwatch.com/investing/stock/" + ticker)
			tree = html.fromstring(page.content)
			price = tree.xpath("/html/body/div[1]/div[3]/div[2]/div/div/div[2]/h3/bg-quote/text()")
			return round(float(price[0]), 2)
		except:
			return None

	def buy(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		return self.orderDriver(ticker, shares, term, priceType, price, OrderType.BUY)

	def short(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		return self.orderDriver(ticker, shares, term, priceType, price, OrderType.SHORT)

	def sell(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		return self.orderDriver(ticker, shares, term, priceType, price, OrderType.SELL)

	def cover(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
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
			print("Debug mode is enabled; payload is: " + str(payload))
			return None
		else:
			url = ('http://www.marketwatch.com/game/%s/trade/submitorder' % self.game)
			headers = {'Content-Type': 'application/json'}
			response = json.loads((self.session.post(url=url, headers=headers, json=payload)).text)
			return(response)

	def cancelOrder(self, id):
		url = ('http://www.marketwatch.com/game/' + self.game + '/trade/cancelorder?id=' + str(id))
		self.session.get(url)
		return None

	def cancelAllOrders(self):
		orders = self.getOrders()
		for order in orders:
			url = ('http://www.marketwatch.com/game/' + self.game + '/trade/cancelorder?id=' + str(order.id))
			self.session.get(url)
		return None

	def getOrders(self):
		tree = html.fromstring(self.session.get("http://www.marketwatch.com/game/" + self.game + "/portfolio/orders").content)
		rawOrders = tree.xpath("//*[@id=\"maincontent\"]/section[2]/table/tbody")
		orders = []
		try:
			numberOfOrders = len(rawOrders[0])
		except:
			return orders
		for i in range(numberOfOrders):
			cleanedId = self.cleanText(rawOrders[0][i][4][0].get("href"))
			id = int(cleanedId[cleanedId.index('=') + 1:])
			ticker = self.cleanText(rawOrders[0][i][0][0].text)
			quantity = int(self.cleanText(rawOrders[0][i][1].text))
			orderType = self.getOrderType(self.cleanText(rawOrders[0][i][2].text))
			priceType = self.getPriceType(self.cleanText(rawOrders[0][i][2].text))
			price = self.getPriceOfOrder(self.cleanText(rawOrders[0][i][2].text))
			orders.append(Order(id, ticker, quantity, orderType, priceType, price))
		return orders

	def cleanText(self, text):
		return text.replace("\r\n", "").replace("\t", "").replace(" ", "").replace(",", "")

	def getOrderType(self, order):
		if ("Buy" in order):
			return OrderType.BUY
		elif ("Short" in order):
			return OrderType.SHORT
		elif ("Cover" in order):
			return OrderType.COVER
		elif ("Sell" in order):
			return OrderType.SELL
		else:
			return None

	def getPriceType(self, order):
		if ("market" in order):
			return PriceType.MARKET
		elif ("limit" in order):
			return PriceType.LIMIT
		elif ("stop" in order):
			return PriceType.STOP
		else:
			return None

	def getPriceOfOrder(self, order):
		if ("$" not in order):
			return None
		else:
			return float(order[(order.index('$') + 1):])

	def getPositions(self):
		tree = html.fromstring(self.session.get("http://www.marketwatch.com/game/" + self.game + "/portfolio/Holdings").content)
		rawPositions = tree.xpath("//*[@id=\"maincontent\"]/section[2]/div[1]/table/tbody")
		positions = []
		try:
			numberOfPositions = len(rawPositions[0])
		except:
			return positions
		for i in range(numberOfPositions):
			currentItem = rawPositions[0][i]
			positions.append(Position(currentItem.get('data-ticker'), self.getOrderType(currentItem.get('data-type')), int(float(currentItem.get('data-shares')))))
		return positions

	def getBuyingPower(self):
		tree = html.fromstring(self.session.get("http://www.marketwatch.com/game/" + self.game + "/portfolio/Holdings").content)
		buyingPower = tree.xpath("//*[@id=\"maincontent\"]/section[1]/div[2]/ul[2]/li[1]/span[2]/text()")[0]
		buyingPower = buyingPower.replace("$", "").replace(",", "")
		return float(buyingPower)

	def getCashRemaining(self):
		tree = html.fromstring(self.session.get("http://www.marketwatch.com/game/" + self.game + "/portfolio/Holdings").content)
		cashRemaining = tree.xpath("//*[@id=\"maincontent\"]/section[1]/div[2]/ul[2]/li[2]/span[2]/text()")[0]
		cashRemaining = cashRemaining.replace("$", "").replace(",", "")
		return float(cashRemaining)

	def getCashBorrowed(self):
		tree = html.fromstring(self.session.get("http://www.marketwatch.com/game/" + self.game + "/portfolio/Holdings").content)
		cashBorrowed = tree.xpath("//*[@id=\"maincontent\"]/section[1]/div[2]/ul[2]/li[3]/span[2]/text()")[0]
		cashBorrowed = cashBorrowed.replace("$", "").replace(",", "")
		return float(cashBorrowed)

	def getExecutionPrice(self):
		tree = html.fromstring(self.session.get("http://www.marketwatch.com/game/" + self.game + "/portfolio/transactionhistory").content)
		price = self.cleanText(tree.xpath("//*[@id=\"maincontent\"]/section[2]/div[1]/table/tbody/tr[1]/td[6]/text()")[0]).replace("$", "")
		return float(price)