"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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
import logging
from abc import ABCMeta, abstractmethod

from programy.clients.client import BotClient
from programy.config.sections.client.rest import RestConfiguration

class RestBotClient(BotClient):
    __metaclass__ = ABCMeta

    def __init__(self, clientid, argument_parser=None):
        BotClient.__init__(self, clientid, argument_parser)
        self.api_keys = []

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "REST")

    def get_client_configuration(self):
        return RestConfiguration()

    def load_api_keys(self):
        if self.configuration.client_configuration.api_key_file is not None:
            with open(self.configuration.client_configuration.api_key_file, "r", encoding="utf-8") as api_key_file:
                for api_key in api_key_file:
                    self.api_keys.append(api_key.strip())

    def initialise(self):
        self.load_api_keys()

    @abstractmethod
    def get_api_key(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def get_question(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def get_sessionid(self, rest_request):
        raise NotImplementedError()

    def is_apikey_valid(self, apikey):
        return bool(apikey in self.api_keys)

    def verify_api_key_usage(self, request):
        if self.configuration.client_configuration.use_api_keys is True:

            apikey = self.get_api_key(request)

            if apikey is None:
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("Unauthorised access - api required but missing")
                return {'error': 'Unauthorized access'}, 401

            if self.is_apikey_valid(apikey) is False:
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("'Unauthorised access - invalid api key")
                return {'error': 'Unauthorized access'}, 401

        return None, None

    def format_success_response(self, sessionid, question, answer):
        return {"question": question, "answer": answer, "sessionid": sessionid}

    def format_error_response(self, sessionid, question, error):
        return {"question": question, "answer": self.bot.default_response, "sessionid": sessionid, "error": error}

    def ask_question(self, sessionid, question):
        return self.bot.ask_question(sessionid, question, responselogger=self)

    def process_request(self, request):
        question = "Unknown"
        sessionid = "Unknown"
        try:
            response, status = self.verify_api_key_usage(request)
            if response is not None:
                return response, status

            question = self.get_question(request)
            sessionid = self.get_sessionid(request)

            response = self.ask_question(sessionid, question)

            return self.format_success_response(sessionid, question, response), 200

        except Exception as excep:

            return self.format_error_response(sessionid, question, str(excep)), 500
