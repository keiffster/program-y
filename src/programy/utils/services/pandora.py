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
from xml.etree import ElementTree

from programy.utils.services.service import Service
from programy.config.brain import BrainServiceConfiguration
from programy.utils.services.requestsapi import RequestsAPI

class PandoraService(Service):

    default_url = 'http://www.pandorabots.com/pandora/talk-xml'

    def __init__(self, config: BrainServiceConfiguration):
        Service.__init__(self, config)

    def ask_question(self, bot, clientid: str, question: str):
        try:
            # TODO move this into license.keys
            botid = self._config.parameter('botid')

            payload = {'botid': botid, 'input': question}
            response = RequestsAPI.get(PandoraService.default_url, params=payload)

            if response is None:
                raise Exception("No response from service")

            tree = ElementTree.fromstring(response.content)

            that = tree.find("that")
            if that is None:
                raise Exception("Invalid response from service, no 'that'")

            return that.text

        except Exception as excep:
            logging.error(str(excep))
            return ""

if __name__ == '__main__':

    def run():
        service_config = BrainServiceConfiguration("PANDORA")
        service_config.set_parameter('botid', "f5d922d97e345aa1")

        service = PandoraService(service_config)
        service_response = service.ask_question(None, "testid", "What does a cat look like") #"What is a cat")
        print(service_response)

    run()
