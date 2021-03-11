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
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException
from programy.utils.logging.ylogger import YLogger


class MirosoftSearchQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return MirosoftSearchQuery(service)

    def parse_matched(self, matched):
        self._query = ServiceQuery._get_matched_var(matched, 0, "query")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._query = None

    def execute(self):
        return self._service.search(self._query)

    def aiml_response(self, response):
        payload = response['response']['payload']
        webPages = payload['webPages']
        values = webPages['value']
        result = "<ul>\n"
        result += "\n".join(["<li>{0}</li>".format(x['snippet']) for x in values])
        result += "</ul>"
        return result


class MicrosoftSearchServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class MicrosoftSearchService(RESTService):
    """
    https://portal.azure.com/
    """
    PATTERNS = [
        [r"SEARCH\s(.+)", MirosoftSearchQuery]
    ]

    BASE_SEARCH_URL="https://chatilly.cognitiveservices.azure.com/bing/v7.0"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._key = None
        
    def initialise(self, client):
        self._key = client.license_keys.get_key('BING_SEARCH_KEY')
        if self._key is None:
            YLogger.error(self, "BING_SEARCH_KEY missing from license.keys, service will not function correctly!")

    def patterns(self) -> list:
        return MicrosoftSearchService.PATTERNS

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "search.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "search.conf"

    def _build_search_url(self, query):
        if self.configuration.url is not None:
            url = self.configuration.url

        else:
            url = MicrosoftSearchService.BASE_SEARCH_URL

        url += "/search?q={0}".format(urllib.parse.quote(query))
        return url

    def _build_search_headers(self):
        return {"Ocp-Apim-Subscription-Key": self._key}

    def search(self, query):
        url = self._build_search_url(query)
        headers = self._build_search_headers()
        response = self.query('search', url, headers=headers)
        return response

    def _response_to_json(self, api, response):
        return response.json()
