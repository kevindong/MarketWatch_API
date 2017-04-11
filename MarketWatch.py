# NOT READY FOR USAGE
# DO NOT USE

import json
import requests
import os
from enum import Enum

class MarketWatch:
	def __init__(self):
		self.session = requests.Session()

	class Term(Enum):
		DAY = 1
		INDEFINITE = 2

	class PriceType(Enum):
		MARKET = 1
		LIMIT = 2
		STOP = 3

	terms = {
		Term.DAY: '"DayOrder"',
		Term.INDEFINITE: '"Cancelled"'
	}

	def login(self, email, password):
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
			exit(1)

	def getPrice(ticker):
		try:
			page = requests.get("http://www.marketwatch.com/investing/fund/%s" % ticker)
			tree = html.fromstring(page.content)
			price = tree.xpath("/html/body/div[1]/div[3]/div[2]/div/div/div[2]/h3/bg-quote/text()")
			return round(float(price[0]), 2)
		except:
			return None

	def buy(ticker, shares, term, priceType):
		if (priceType != PriceType.MARKET):
			print('This function call is only for orders with market pricing.')
			exit(1)
		return buy(ticker, shares, term, priceType, None)

	def buy(ticker, shares, term, priceType, price):
		payload = [{"Fuid": ticker, "Shares": shares, "Type": "Buy", "Term": terms[priceType]}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = price
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = price
		return payload

	def short(ticker, shares, term, priceType):
		if (priceType != PriceType.MARKET):
			print('This function call is only for orders with market pricing.')
			exit(1)
		return short(ticker, shares, term, priceType, None)

	def short(ticker, shares, term, priceType, price):
		payload = [{"Fuid": ticker, "Shares": shares, "Type": "Short", "Term": terms[priceType]}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = price
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = price
		return payload

	def sell(ticker, shares, term, priceType):
		if (priceType != PriceType.MARKET):
			print('This function call is only for orders with market pricing.')
			exit(1)
		return sell(ticker, shares, term, priceType, None)

	def sell(ticker, shares, term, priceType, price):
		# TODO: ensure user actually owns the shares
		payload = [{"Fuid": ticker, "Shares": shares, "Type": "Sell", "Term": terms[priceType]}]
		if (priceType == PriceType.LIMIT):
			payload[0]['Limit'] = price
		if (priceType == PriceType.STOP):
			payload[0]['Stop'] = price
		return payload

	#def cover(ticker, shares, term, priceType):

email = ''
password = ''

try:
	email = os.environ['MARKETWATCH_EMAILd']
	password = os.environ['MARKETWATCH_PASSWORDd']
	print('Your credentials have been successfully read from your env variables.')
except KeyError:
	print('You have not set your MarketWatch credentials in your env variables.\n'
		+ 'Please input your credentials for this session now.')
	email = input('Email: ')
	password = input('Password: ')
	print('Your credentials have been successfully saved for just this session.')

api = MarketWatch()
api.login(email, password)