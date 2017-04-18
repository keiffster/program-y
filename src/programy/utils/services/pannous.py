"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import logging

from programy.utils.services.service import Service
from programy.config.brain import BrainServiceConfiguration
from programy.utils.services.requestsapi import RequestsAPI

class PannousService(Service):

    default_url = 'http://weannie.pannous.com/api'

    def __init__(self, config):
        Service.__init__(self, config)

    def ask_question(self, bot, clientid: str, question: str):
        try:
            # TODO possibly move this into license.keys
            login = self._config.parameter('login')

            payload = {'input': question, 'login': login}

            response = RequestsAPI.get(PannousService.default_url, params=payload)
            json_data = response.json()

            if 'output' not in json_data:
                raise Exception("'output' section missing from pannous json_data")

            if len(json_data["output"]) == 0:
                raise Exception("'output' section has no elements in pannous json_data")

            if 'actions' not in json_data["output"][0]:
                raise Exception("'actions' section in output[0] in pannous json_data")

            if 'say' not in json_data["output"][0]['actions']:
                raise Exception("'say' section missing from output[0]['actions'] in pannous json_data")

            if 'text' not in json_data["output"][0]['actions']['say']:
                raise Exception("text' section missing from output[0]['actions']['say'] in pannous json_data")

            return json_data["output"][0]['actions']['say']['text']

        except Exception as excep:
            logging.error(str(excep))
            return ""

# Integration Test
if __name__ == '__main__':

    def run():
        service_config = BrainServiceConfiguration("PANNOUS")
        service_config.set_parameter('login', "test-user")

        service = PannousService(service_config)
        service_response = service.ask_question(None, "testid", "What does a cat look like") # "What is a cat")
        print(service_response)

    run()
