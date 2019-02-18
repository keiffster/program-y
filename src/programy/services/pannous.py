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

from programy.services.service import Service
from programy.config.brain.service import BrainServiceConfiguration
from programy.services.requestsapi import RequestsAPI


class PannousAPI(object):

    def __init__(self, request_api=None):
        if request_api is None:
            self._requests_api = RequestsAPI()
        else:
            self._requests_api = request_api

    def ask_question(self, url, question, login):
        payload = {'input': question, 'login': login}

        response = self._requests_api.get(url, params=payload)
        if response is None:
            raise Exception("No response from pannous service")

        json_data = response.json()

        if 'output' not in json_data:
            raise Exception("'output' section missing from pannous json_data")

        if json_data["output"] is None or not json_data["output"]:
            raise Exception("'output' section has no elements in pannous json_data")

        if 'actions' not in json_data["output"][0]:
            raise Exception("'actions' section in output[0] in pannous json_data")

        if 'say' not in json_data["output"][0]['actions']:
            raise Exception("'say' section missing from output[0]['actions'] in pannous json_data")

        if 'text' not in json_data["output"][0]['actions']['say']:
            raise Exception("'text' section missing from output[0]['actions']['say'] in pannous json_data")

        return json_data["output"][0]['actions']['say']['text']


class PannousService(Service):

    LICENSE_KEY = 'PANNOUS_LOGIN'

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = PannousAPI()
        else:
            self.api = api

        self.url = None
        if config.url is None:
            raise Exception("Undefined url parameter")
        else:
            self.url = config.url

    def ask_question(self, client_context, question: str):
        try:
            if client_context.client.license_keys.has_key(PannousService.LICENSE_KEY):
                login = client_context.client.license_keys.get_key(PannousService.LICENSE_KEY)
            else:
                YLogger.error(client_context, "No variable %s found in license key file", PannousService.LICENSE_KEY)
                return ""

            return self.api.ask_question(self.url, question, login)

        except Exception as excep:
            YLogger.error(client_context, str(excep))
            return ""
