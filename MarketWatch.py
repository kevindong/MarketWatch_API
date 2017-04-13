# NOT READY FOR USAGE
# DO NOT USE

import json
import requests
from enum import Enum
from lxml import html

class Term(Enum):
	DAY = 1
	INDEFINITE = 2

class PriceType(Enum):
	MARKET = 1
	LIMIT = 2
	STOP = 3

class SecurityType(Enum):
	ETF = 1
	STOCK = 2

class MarketWatch:
	terms = {
		Term.DAY: 'DayOrder',
		Term.INDEFINITE: 'Cancelled'
	}

	def __init__(self, email, password, game):
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

	def getType(self, ticker):
		page = requests.get("http://www.marketwatch.com/investing/stock/%s" % ticker)
		if ("fund" in page.url):
			return SecurityType.ETF
		else:
			return SecurityType.STOCK

	def buy(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user has enough money
		ticker = self.formalizeTicker(ticker)
		payload = [{"Fuid": ticker, "Shares": str(shares), "Type": "Buy", "Term": self.terms[term]}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = str(price)
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = str(price)
		return self.submit(payload)

	def short(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user has enough money
		ticker = self.formalizeTicker(ticker)
		payload = [{"Fuid": ticker, "Shares": str(shares), "Type": "Short", "Term": self.terms[term]}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = str(price)
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = str(price)
		return self.submit(payload)

	def sell(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user actually owns the shares
		ticker = self.formalizeTicker(ticker)
		payload = [{"Fuid": ticker, "Shares": str(shares), "Type": "Sell", "Term": self.terms[term]}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = str(price)
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = str(price)
		return self.submit(payload)

	def cover(self, ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None):
		# TODO: ensure user actually has a short position
		ticker = self.formalizeTicker(ticker)
		payload = [{"Fuid": ticker, "Shares": str(shares), "Type": "Cover", "Term": self.terms[term]}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = str(price)
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = str(price)
		return self.submit(payload)

	def formalizeTicker(self, ticker):
		if (self.getType(ticker) == SecurityType.ETF):
			return ('EXCHANGETRADEDFUND-XASQ-%s' % ticker)
		else:
			return ('STOCK-XASQ-%s' % ticker)

	def submit(self, payload):
		url = ('http://www.marketwatch.com/game/%s/trade/submitorder' % self.game)
		headers = {'Content-Type': 'application/json'}
		response = json.loads((self.session.post(url=url, headers=headers, json=payload)).text)
		return(response)