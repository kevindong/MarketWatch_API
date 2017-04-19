# MarketWatch API
A Python wrapper for interacting with the Games section of MarketWatch.

This wrapper works by reverse engineering how the MarketWatch website works. Consequently, this wrapper is very fragile and depends on MarketWatch not changing their website.

# Usage
Use this API by putting `from MarketWatch import *` into your implementation. See `driver.py` as an example usage for this wrapper.

## Helper Classes
* `Term`: enum for order validity. Options are `DAY` and `INDEFINITE`.
* `PriceType`: enum for order price type. Options are `MARKET`, `LIMIT`, and `STOP`.
* `OrderType`: enum for order type. Options are `BUY`, `SELL`, `SHORT`, and `COVER`.
* `Order`: holder for order information. 
  * `id`: the id of the order, used for canceling orders.
  * `ticker`: the normal ticker of the order (such as `AAPL` for Apple).
  * `quantity`: number of shares the order is for.
  * `orderType`: a way to store the `OrderType` enum.
  * `priceType`: a way to store the `PriceType` enum.
  * `price`: the price of the order, if applicable.

## Main Class (`MarketWatch`)
### Constructor
Call with `MarketWatch(email, password, game, debugMode = False)`. 

* `email`: the email of your account.
* `password`: the password of your account.
* `game`: the ID of the game you're in.
* `debugMode`: if `True`, orders will not submitted. Optional parameter; default is to not be in debug mode.

### Methods
* `getPrice(ticker)`: gets the price of the security with the inputted ticker. `ticker` would be something like `AAPL`.
* `<order>(ticker, shares, term = Term.INDEFINITE, priceType = PriceType.MARKET, price = None)`
  * `ticker` and `shares` are mandatory. You may omit parameters if desired. However, you must include all parameters prior to the one you want to use (i.e. to use `priceType`, you must specify `term`). You must specify `price` for certain `priceType`s (`LIMIT` and `STOP`). If the optional parameters are not specified, the default (as shown above) will be used.
  * `order` can be `buy`, `sell`, `short`, and `cover`.
  * `ticker`: the normal ticker of the order (such as `AAPL` for Apple).
  * `shares`: the number of shares the order is for.
  * `term`: enum for order validity. Options are `DAY` and `INDEFINITE`.
  * `priceType`: enum for order price type. Options are `MARKET`, `LIMIT`, and `STOP`.
  * `price`: the price of the order, if applicable. Otherwise, feel free to omit or pass in `None`.
* `cancelOrder(id)`: cancels the order with the inputted `id`. This value is found in the `Order` class.
* `cancelAllOrders()`: cancels all currently pending orders.
* `getOrders()`: returns a list of `Order` objects. Each of which stands for one pending order you currently have, as displayed on MarketWatch. Only grabs orders on the first page (should be 10).
* `getBuyingPower()`: gets buying power.
* `getCashRemaining()`: gets cash remaining.
* `getCashBorrowed()`: gets cash borrowed.
* `getExecutionPrice()`: gets the price at which the most recently processed order executed at.

The following methods are not intended for use by you.

* `orderDriver(ticker, shares, term, priceType, price, orderType)`: all the `<order>` methods internally call this. 
* `submit(payload)`: Receives the order to be submitted to MarketWatch for processing from orderDriver.
* `validateTicker(ticker)`: converts normal tickers (`AAPL`) to how it's referred to on MarketWatch internally (`STOCK-XNAS-AAPL`).
* `cleanText(text)`: strips out whitespace and junk characters from text.
* `getOrderType(order)`: used in `getOrders()` to determine order type (buy, sell, short, or cover).
* `getPriceOfOrder(order)`: used in `getOrders()` to determine the price of the order.

# Version History
## 1.0.0
Initial release.

# License
Apache License, Version 2.0

Copyright 2017 Kevin Dong

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.