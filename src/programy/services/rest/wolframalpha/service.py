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
import urllib.parse
import os
import json
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class WolframAlphaSimpleQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return WolframAlphaSimpleQuery(service)

    def parse_matched(self, matched):
        self._query = ServiceQuery._get_matched_var(matched, 0, "query")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._query = None

    def execute(self):
        return self._service.simple(self._query)

    def aiml_response(self, response):
        result = WolframAlphaSimpleQuery.get_answer(response)
        if result is not None:
            YLogger.debug(self, result)
            return result

        return None

    @staticmethod
    def get_answer(data):
        response = data.get('response', None)
        if response is not None:
            payload = response.get('payload', None)
            if payload is not None:
                queryresult = payload.get('queryresult', None)
                if queryresult is not None:
                    pods = queryresult.get('pods', [])
                    for pod in pods:
                        title = pod.get('title', "")
                        if title == 'Input interpretation':
                            subpods = pod.get('subpods', [])
                            if subpods:
                                return "SIMPLE {0}".format(subpods[0].get('plaintext', None))
        return None


class WolframAlphaShortQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return WolframAlphaShortQuery(service)

    def parse_matched(self, matched):
        self._query = ServiceQuery._get_matched_var(matched, 0, "query")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._query = None

    def execute(self):
        return self._service.short(self._query)

    def aiml_response(self, response):
        payload = response['response']['payload']
        result = "SHORT {0}".format(payload['answer'])
        YLogger.debug(self, result)
        return result


class WolframAlphaServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class WolframAlphaService(RESTService):
    """
    """
    PATTERNS = [
        [r"SIMPLE\s(.+)", WolframAlphaSimpleQuery],
        [r"SHORT\s(.+)?", WolframAlphaShortQuery]
    ]

    SIMPLE_QUERY_URL = "https://api.wolframalpha.com/v1/query"
    SHORT_QUERY_URL = "https://api.wolframalpha.com/v1/result"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._appID = None

    def patterns(self) -> list:
        return WolframAlphaService.PATTERNS

    def initialise(self, client):
        self._appID = client.license_keys.get_key("WOLFRAM_ALPHA_APPID")
        if self._appID is None:
            YLogger.error(self, "WOLFRAM_ALPHA_APPID missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "wolframalpha.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "wolframalpha.conf"

    def _build_simple_url(self, question):
        url = WolframAlphaService.SIMPLE_QUERY_URL
        url += "?input={0}".format(urllib.parse.quote_plus(question))
        url += "&appid={0}".format(self._appID)
        url += "&output=json"
        url += "&format=plaintext"
        return url

    def _build_short_url(self, question):
        url = WolframAlphaService.SHORT_QUERY_URL
        url += "?i={0}".format(urllib.parse.quote_plus(question))
        url += "&appid={0}".format(self._appID)
        return url

    def simple(self, question):
        url = self._build_simple_url(question)
        response = self.query('simple', url)
        return response

    def short(self, question):
        url = self._build_short_url(question)
        response = self.query('short', url)
        return response

    def _response_to_json(self, api, response):

        if api == 'short':
            return {"answer": response.text}

        elif api == 'simple':
            return json.loads(response.text)

        return None
