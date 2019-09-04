"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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
from programy.utils.logging.ylogger import YLogger
from programy.clients.restful.config import RestConfiguration


class APIKeysHandler(object):

    API_KEY_HEADER = "PROGRAMY-API-KEY"
    API_KEY_ARG = 'apikey'

    def __init__(self, configuration: RestConfiguration):
        self._configuration = configuration
        self.api_keys = []

    @staticmethod
    def format_get_api_key_param(api_key):
        return "%s=%s" % (APIKeysHandler.API_KEY_ARG, api_key)

    @staticmethod
    def add_post_api_key_header(headers, api_key):
        headers['PROGRAMY-API-KEY'] = api_key

    def load_api_keys(self):
        if self._configuration.use_api_keys is True:
            if self._configuration.api_key_file is not None:
                try:
                    with open(self._configuration.api_key_file, "r", encoding="utf-8") as api_key_file:
                        for api_key in api_key_file:
                            self.api_keys.append(api_key.strip())

                except Exception as excep:
                    YLogger.exception(self, "Failed to open license key file [%s]", excep, self._configuration.api_key_file)

    def use_api_keys(self):
        return self._configuration.use_api_keys

    def get_api_key(self, rest_request, method='GET'):
        if method == 'GET':
            if APIKeysHandler.API_KEY_ARG not in rest_request.args:
                return None

            if rest_request.args[APIKeysHandler.API_KEY_ARG] is None:
                return None

            return rest_request.args[APIKeysHandler.API_KEY_ARG]

        elif method == 'POST':
            if APIKeysHandler.APIKeysHandler not in rest_request.headers or \
                    rest_request.headers [APIKeysHandler.APIKeysHandler] is None:
                return None

            return rest_request.headers [APIKeysHandler.APIKeysHandler]

        return None

    def is_apikey_valid(self, apikey):
        return bool(apikey in self.api_keys)

    def verify_api_key_usage(self, request, method='GET'):
        if self.use_api_keys() is True:
            apikey = self.get_api_key(request, method)

            if apikey is None:
                YLogger.error(self, "Unauthorised access - api required but missing")
                return False

            if self.is_apikey_valid(apikey) is False:
                YLogger.error(self, "'Unauthorised access - invalid api key")
                return False

        return True

