# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.decimal_to_precision import DECIMAL_PLACES


class bitclude(Exchange):

    def describe(self):
        return self.deep_extend(super(bitclude, self).describe(), {
            'id': 'bitclude',
            'name': 'Bitclude',
            'countries': ['PL'],
            'rateLimit': 2000,
            'certified': False,
            'pro': False,
            'urls': {
                'api': {
                    'public': 'https://api.bitclude.com/',
                    'private': 'https://api.bitclude.com/',
                },
                'www': 'https://bitclude.com',
                'doc': 'https://docs.bitclude.com',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
                'uid': True,
            },
            'has': {
                'fetchMarkets': 'emulated',
                'fetchCurrencies': True,  # private
                'cancelAllOrders': False,
                'fetchClosedOrders': False,
                'createDepositAddress': True,
                'fetchDepositAddress': 'emulated',
                'fetchDeposits': True,
                'fetchFundingFees': 'emulated',
                'fetchMyTrades': True,
                'fetchOHLCV': False,
                'fetchOpenOrders': True,
                'fetchOrder': False,
                'fetchOrderBook': True,
                'fetchOrders': False,
                'fetchTickers': True,
                'fetchTicker': 'emulated',
                'fetchTrades': True,
                'fetchTradingFees': False,
                'fetchWithdrawals': False,
                'withdraw': False,
            },
            'api': {
                'public': {
                    'get': [
                        'stats/ticker.json',
                        'stats/orderbook_{base}{quote}.json',
                        'stats/history_{base}{quote}.json',
                    ],
                },
                'private': {
                    'get': [
                        '',
                    ],
                },
            },
            'exceptions': {
                # stolen, todo rewrite
                'exact': {
                    'Not enough balances': InsufficientFunds,  # {"error":"Not enough balances","success":false}
                    'InvalidPrice': InvalidOrder,  # {"error":"Invalid price","success":false}
                    'Size too small': InvalidOrder,  # {"error":"Size too small","success":false}
                    'Missing parameter price': InvalidOrder,  # {"error":"Missing parameter price","success":false}
                    'Order not found': OrderNotFound,  # {"error":"Order not found","success":false}
                },
                'broad': {
                    'Invalid parameter': BadRequest,  # {"error":"Invalid parameter start_time","success":false}
                    'The requested URL was not found on the server': BadRequest,
                    'No such coin': BadRequest,
                    'No such market': BadRequest,
                    'An unexpected error occurred': ExchangeError,  # {"error":"An unexpected error occurred, please try again later(58BC21C795).","success":false}
                },
            },
            'precisionMode': DECIMAL_PLACES,
        })

    def fetch_markets(self, params={}):
        response = self.publicGetStatsTickerJson(params)
        result = []
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            baseId, quoteId = id.split('_')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = (base + '/' + quote)
            precision = {
                'price': None,
                'amount': None,
            }
            info = {}
            info[id] = self.safe_value(response, id)
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': None,
                'info': info,
            }
            result.append(entry)
        return result

    def fetch_currencies(self, params={}):
        if not self.apiKey or not self.uid:
            raise AuthenticationError(self.id + " fetchCurrencies is an authenticated endpoint, therefore it requires 'apiKey' and 'uid' credentials. If you don't need currency details, set exchange.has['fetchCurrencies'] = False before calling its methods.")
        request = {
            'method': 'account',
            'action': 'getwalletsstatus',
        }
        response = self.privateGet(self.extend(request, params))
        ids = list(response.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            if id == 'success':
                continue
            currency = response[id]
            code = self.safe_currency_code(id)
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': None,
                'active': self.safe_value(currency, 'is_online'),
                'fee': self.safe_float(currency, 'current_optimal_fee'),
                'precision': self.safe_integer(currency, 'decimal_point'),
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': self.safe_float(currency, 'current_minimal_amount'),
                        'max': None,
                    },
                },
            }
        return result

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        symbols = self.symbols if (symbols is None) else symbols
        tickers = self.publicGetStatsTickerJson(params)
        marketIds = list(self.marketsById.keys())
        result = {}
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            market = self.marketsById[marketId]
            symbol = market['symbol']
            ticker = self.safe_value(tickers, marketId)
            if self.in_array(symbol, symbols):
                result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        ticker = self.fetch_tickers([symbol])
        return self.safe_value(ticker, symbol)

    def parse_ticker(self, ticker, market):
        timestamp = self.milliseconds()
        symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'max24H'),
            'low': self.safe_float(ticker, 'min24H'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': self.safe_float(ticker, 'last'),
            'last': self.safe_float(ticker, 'last'),
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        baseId, quoteId = market['id'].split('_')
        request = {
            'base': baseId,
            'quote': quoteId,
        }
        response = self.publicGetStatsOrderbookBaseQuoteJson(self.extend(request, params))
        data = self.safe_value(response, 'data')
        timestamp = self.safe_timestamp(data, 'timestamp')
        parsedOrderBook = self.parse_order_book(response, timestamp, 'bids', 'asks', 1, 0)
        if limit is not None:
            parsedOrderBook['bids'] = self.filter_by_since_limit(parsedOrderBook['bids'], None, limit)
            parsedOrderBook['asks'] = self.filter_by_since_limit(parsedOrderBook['asks'], None, limit)
        return parsedOrderBook

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'base': market['baseId'],
            'quote': market['quoteId'],
        }
        response = self.publicGetStatsHistoryBaseQuoteJson(self.extend(request, params))
        trades = self.safe_value(response, 'history')
        return self.parse_trades(trades, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'method': 'account',
            'action': 'history',
        }
        response = self.privateGet(self.extend(request, params))
        trades = self.safe_value(response, 'history', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_trade(self, trade, market=None):
        #  fetchTrades
        #
        #    {
        #         "time":1531917229,
        #         "nr":"786",
        #         "amount":"0.00018620",
        #         "price":"7314.57",
        #         "type":"a"
        #    }
        #
        #  fetchMyTrades
        #
        #    {
        #         "currency1": "btc",
        #         "currency2": "usd",
        #         "amount": "0.00100000",
        #         "time_close": 1516212758,
        #         "price": "4.00",
        #         "fee_taker": "50",  # Idk what does it exactly means
        #         "fee_maker": "0",
        #         "type": "bid",
        #         "action": "open"
        #    }
        id = self.safe_string(trade, 'nr')
        timestamp = self.safe_integer_2(trade, 'time', 'time_close')
        if 'time' in trade:
            # API return timestamp in different formats depending on endpoint. Of course self isn't specified in docs xD
            timestamp = timestamp * 1000
        type = None
        baseId = self.safe_string(trade, 'currency1')
        quoteId = self.safe_string(trade, 'currency2')
        symbol = None
        quote = None
        if baseId is not None and quoteId is not None:
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = (base + '/' + quote)
        else:
            symbol = market['symbol']
            quote = market['quote']
        side = self.safe_string(trade, 'type')
        if side == 'a' or side == 'ask':
            side = 'sell'
        elif side == 'b' or side == 'bid':
            side = 'buy'
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
                if self.currency(quote)['precision'] is not None:
                    cost = self.currency_to_precision(quote, cost)
        fee = None  # todo
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'order': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_balance(self, params={}):
        self.load_markets()
        request = {
            'method': 'account',
            'action': 'info',
        }
        response = self.privateGet(self.extend(request, params))
        result = {
            'info': response,
        }
        balances = self.safe_value(response, 'balances', [])
        currencies = list(balances.keys())
        for i in range(0, len(currencies)):
            balance = self.safe_value(balances, currencies[i])
            currencyCode = self.safe_currency_code(currencies[i])
            account = self.account()
            account['free'] = self.safe_float(balance, 'active')
            account['used'] = self.safe_float(balance, 'inactive')
            result[currencyCode] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        orderId = None
        response = None
        feeCost = None
        feeCurrency = None
        if type == 'limit':
            request = {
                'method': 'transactions',
                'action': side,
                'market1': market['baseId'],
                'market2': market['quoteId'],
                'amount': self.currency_to_precision(market['base'], amount),
                'rate': self.currency_to_precision(market['quote'], price),
            }
            response = self.privateGet(self.extend(request, params))
            order = self.safe_value(response, 'actions')
            orderId = self.safe_string(order, 'order')
        elif type == 'market':
            request = {
                'method': 'account',
                'action': 'convert',
            }
            request['market1'] = market['baseId'] if (side == 'sell') else market['quoteId']
            request['market2'] = market['quoteId'] if (side == 'sell') else market['baseId']
            currencyOfAmount = market['base'] if (side == 'sell') else market['quote']
            request['amount'] = self.currency_to_precision(currencyOfAmount, amount)
            response = self.privateGet(self.extend(request, params))
            feeCurrency = market['quote'] if (side == 'sell') else market['base']
            feeCost = self.safe_string(response, 'fee')
        timestamp = self.milliseconds()
        return {
            'id': orderId,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': 'open',
            'symbol': market['symbol'],
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': None,
            'fee': {
                'currency': feeCurrency,
                'cost': feeCost,
                'rate': None,
            },
            'trades': None,
            'info': response,
        }

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            'method': 'account',
            'action': 'activeoffers',
        }
        response = self.privateGet(self.extend(request, params))
        result = self.safe_value(response, 'offers', [])
        orders = self.parse_orders(result, None, since, limit)
        if symbol is not None:
            orders = self.filter_by(orders, 'symbol', symbol)
        return orders

    def parse_order(self, order, market=None):
        # due to very diverse structure of orders self method only work for these returned by fetchOpenOrders
        status = 'open'
        side = self.safe_string(order, 'offertype')
        if side == 'ask':
            side = 'sell'
        elif side == 'bid':
            side = 'buy'
        symbol = None
        if market is None:
            baseId = self.safe_string(order, 'currency1')
            quoteId = self.safe_string(order, 'currency2')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = (base + '/' + quote)
        else:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'time_open')
        return {
            'info': order,
            'id': self.safe_string(order, 'nr'),
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': self.safe_float(order, 'price'),
            'amount': self.safe_float(order, 'amount'),
            'remaining': None,
            'filled': None,
            'status': status,
            'fee': None,
            'cost': None,
            'trades': None,
        }

    def cancel_order(self, id, symbol=None, params={}):
        side_in_params = ('side' in params)
        if not side_in_params:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a `side` parameter(sell or buy)')
        side = 'bid' if (params['side'] == 'buy') else 'ask'  # Typo could cause cancel wrong order. todo: handle typo
        params = self.omit(params, ['side', 'currency'])
        request = {
            'method': 'transactions',
            'action': 'cancel',
            'order': int(id),
            'typ': side,
        }
        return self.privateGet(self.extend(request, params))

    def cancel_unified_order(self, order, params={}):
        # https://github.com/ccxt/ccxt/issues/6838
        request = {
            'side': order['side'],
        }
        return self.cancel_order(order['id'], None, self.extend(request, params))

    def create_deposit_address(self, code, params={}):
        # not yet documented exchange api method
        self.load_markets()
        currencyId = self.currency_id(code)
        request = {
            'method': 'account',
            'action': 'newaddress',
            'currency': currencyId,
        }
        response = self.privateGet(self.extend(request, params))
        address = self.safe_string(response, 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'info': response,
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currencyId = self.currency_id(code)
        currencyId = currencyId.upper()
        request = {
            'method': 'account',
            'action': 'info',
        }
        response = self.privateGet(self.extend(request, params))
        deposits = self.safe_value(response, 'deposit')
        deposit = self.safe_value(deposits, currencyId)
        address = self.safe_string(deposit, 'deposit')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'info': response,
        }

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchDeposits requires a currency code argument')
        self.load_markets()
        currency = self.currency(code)
        currencyId = currency['id']
        request = {
            'method': 'account',
            'action': 'deposits',
            'currency': currencyId,
        }
        response = self.privateGet(self.extend(request, params))
        transactions = self.safe_value(response, 'history', [])
        return self.parse_transactions(transactions, currency)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchDeposits requires a currency code argument')
        self.load_markets()
        currency = self.currency(code)
        currencyId = currency['id']
        request = {
            'method': 'account',
            'action': 'withdrawals',
            'currency': currencyId,
        }
        response = self.privateGet(self.extend(request, params))
        transactions = self.safe_value(response, 'history', [])
        return self.parse_transactions(transactions, currency)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchDeposits
        #
        #     {
        #       "time": "1530883428",
        #       "amount": "0.13750000",
        #       "type": "b787400027b4eae298bad72150384540a23342daaa3eec1c8d17459c103c6bbc",
        #       "state": "1"
        #     }
        #
        # fetchWithdrawals
        #
        #     {
        #         "time": "1528715035",
        #         "amount": "1.00000000",
        #         "tx": "01b8ae6437843879574b69daf95542aff43a4aefaa90e8f70ebf572eccf01cad",
        #         "address": "2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF",
        #         "state": "0"
        #     },
        #
        timestamp = self.safe_integer(transaction, 'time')
        currencyCode = self.safe_string(currency, 'code')
        amount = self.safe_float(transaction, 'amount')
        address = self.safe_string(transaction, 'address')
        status = self.safe_string(transaction, 'state')  # todo: ask support
        txid = self.safe_string_2(transaction, 'type', 'tx')
        return {
            'info': transaction,
            'id': None,
            'currency': currencyCode,
            'amount': amount,
            'address': address,
            'tag': None,
            'status': status,
            'type': None,
            'updated': None,
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'fee': None,
        }

    def fetch_trading_fees(self, params={}):
        self.load_markets()
        request = {
            'method': 'account',
            'action': 'info',
        }
        response = self.privateGet(self.extend(request, params))
        account = self.safe_value(response, 'account')
        fees = self.safe_value(account, 'fee')
        return {
            'info': response,
            'maker': self.safe_float(fees, 'maker'),
            'taker': self.safe_float(fees, 'taker'),
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + request
        if api == 'private':
            self.check_required_credentials()
            params['id'] = self.uid
            params['key'] = self.apiKey
        if params:
            url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}