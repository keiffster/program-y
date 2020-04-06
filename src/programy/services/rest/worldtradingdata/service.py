"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import json
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class WorldTradingDataStocksServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return WorldTradingDataStocksServiceQuery(service)

    def parse_matched(self, matched):
        self._symbols = ServiceQuery._get_matched_var(matched, 0, "symbols")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._symbols = None

    def execute(self):
        return self._service.stocks(self._symbols)

    def aiml_response(self, response):
        payload = response['response'].get('payload')
        if payload is not None:
            data = payload.get('data')
            if data is not None:
                line = data[0]
                name = line.get('name')
                symbol = line.get('symbol')
                price = line.get('price')
                currency = line.get('currency')

                result = "NAME {0} SYMBOL {1} PRICE {2} CURRENCY {3}".format(name, symbol, price, currency)
                YLogger.debug(self, result)
                return result

        return None


class WorldTradingDataStocksServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class WorldTradingDataStocksService(RESTService):
    """
    "https://www.worldtradingdata.com/home"
    """
    PATTERNS = [
        [r"SYMBOLS\s(.+)", WorldTradingDataStocksServiceQuery]
    ]

    STOCKS_API_URL = "https://api.worldtradingdata.com/api/v1/stock?symbol={0}&api_token={1}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_token = None

    def patterns(self) -> list:
        return WorldTradingDataStocksService.PATTERNS

    def initialise(self, client):
        self._api_token = client.license_keys.get_key('WORLDTRADINGDATA_APITOKEN')
        if self._api_token is None:
            YLogger.error(self, "WORLDTRADINGDATA_APITOKEN missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "worldtradingdata.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "worldtradingdata.conf"

    def _build_symbols_url(self, symbols):
        url = WorldTradingDataStocksService.STOCKS_API_URL.format(symbols, self._api_token)
        return url

    def stocks(self, symbols):
        url = self._build_symbols_url(symbols)
        response = self.query('stocks', url)
        return response

    def _response_to_json(self, api, response):
        return json.loads(response.text)

