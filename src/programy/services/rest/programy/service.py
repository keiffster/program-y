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
from urllib.parse import quote
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class ProgramyServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return ProgramyServiceQuery(service)

    def parse_matched(self, matched):
        self._question = ServiceQuery._get_matched_var(matched, 0, "question")
        self._userid = ServiceQuery._get_matched_var(matched, 1, "userid")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._question = None
        self._userid = None

    def execute(self):
        return self._service.ask(self._question, self._userid)

    def aiml_response(self, response):

        payload = response['response']['payload']

        url = response['response']['url']
        if "v1.0" in url:
            response2 = payload[0]['response']

        elif "v2.0" in url:
            response2 = payload['response']

        else:
            response2 = payload['response']

        result = response2['answer']
        YLogger.debug(self, result)
        return result


class ProgramyServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class ProgramyService(RESTService):
    """
    """
    PATTERNS = [
        [r"ASK\sQUESTION\s(.+)\sUSERID\s(.+)", ProgramyServiceQuery]
    ]

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return ProgramyService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('PROGRAMY_APIKEY')
        if self._api_key is None:
            YLogger.error(self, "PROGRAMY_APIKEY missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "programy.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "programyv1.conf"

    def _build_ask_url(self, question, userid):
        url = self.configuration.url.format(question, userid)
        return url

    def ask(self, question, userid):
        url = self._build_ask_url(question, userid)
        response = self.query('ask', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()
