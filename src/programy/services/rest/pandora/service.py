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
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class PandoraServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return PandoraServiceQuery(service)

    def parse_matched(self, matched):
        self._question = ServiceQuery._get_matched_var(matched, 0, "question")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._question = None

    def execute(self):
        return self._service.ask(self._question)

    def aiml_response(self, response):
        payload = response['response'].get('payload')
        if payload is not None:
            result = format(payload.get('that'))
            YLogger.debug(self, result)
            return result

        return None


class PandoraServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class PandoraService(RESTService):
    """
    http://www.pandorabots.com/pandora/talk-xml?botid=XXX&input=XXX
    """
    PATTERNS = [
        [r"ASK\s(.+)", PandoraServiceQuery]
    ]

    BASE_URL="http://www.pandorabots.com/pandora/talk-xml"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._botid = None

    def patterns(self) -> list:
        return PandoraService.PATTERNS

    def initialise(self, client):
        self._botid = client.license_keys.get_key('PANDORA_BOTID')
        if self._botid is None:
            YLogger.error(self, "PANDORA_BOTID missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "pandora.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "pandora.conf"

    def _build_ask_url(self, question=None):
        url = PandoraService.BASE_URL
        url += "?botid={0}".format(self._botid)
        url += "&input={0}".format(question)
        url += "&format=json"
        return url

    def ask(self, question):
        url = self._build_ask_url(question)
        response = self.query('ask', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

