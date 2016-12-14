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
import requests

from programy.utils.services.service import Service
from programy.config import BrainServiceConfiguration

class GenericRESTService(Service):

    def __init__(self, config):
        Service.__init__(self, config)

    def ask_question(self, bot, clientid: str, question: str):

        payload = {}
        params = self._config.parameters()
        method = "GET"
        host = None
        for param in params:
            if param == 'method':
                method = self._config.parameter(param)
            elif param == 'host':
                host = self._config.parameter(param)
            else:
                payload[param] = self._config.parameter(param)

        if host is None:
            raise Exception("Undefined host parameter")

        try:
            if method == 'GET':
                response = requests.get(host, data=payload)
            elif method == 'POST':
                response = requests.post(host, data=payload)
            else:
                raise Exception("Unsupported REST method [%s]", method)

            if response.status_code != 200:
                logging.error("[%s] return status code [%d]", host, response.status_code)
            else:
                return response.text

        except Exception as excep:
            logging.exception(excep)

        return ""

# Integration Test
if __name__ == '__main__':

    def run():
        service_config = BrainServiceConfiguration("REST")

        service = GenericRESTService(service_config)
        service_response = service.ask_question(None, "testid", "What is a cat")
        print(service_response)

    run()

