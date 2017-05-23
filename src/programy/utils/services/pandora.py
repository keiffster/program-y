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

class PandoraAPI(object):

    def __init__(self, request_api=None):
        if request_api is None:
            self._requests_api = RequestsAPI()
        else:
            self._requests_api = request_api

    def ask_question(self, url, question, botid):
        payload = {'botid': botid, 'input': question}
        response = self._requests_api.get(url, params=payload)

        if response is None:
            raise Exception("No response from pandora service")

        tree = ElementTree.fromstring(response.content)

        that = tree.find("that")
        if that is None:
            raise Exception("Invalid response from pandora service, no <that> element in xml")

        return that.text

class PandoraService(Service):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = PandoraAPI()
        else:
            self.api = api

        self.url = None
        if 'URL' in self._config.parameters():
            self.url = self._config.parameter('URL')
        else:
            raise Exception("Undefined url parameter")

    def ask_question(self, bot, clientid: str, question: str):
        try:
            if bot.license_keys.has_key('PANDORA_BOTID') is True:
                botid = bot.license_keys.get_key('PANDORA_BOTID')
            else:
                logging.error("No variable PANDORA_BOTID found in license key file")
                return ""

            return self.api.ask_question(self.url, question, botid)

        except Exception as excep:
            logging.error(str(excep))
            return ""

