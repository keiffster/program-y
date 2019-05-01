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
from abc import ABCMeta, abstractmethod

from programy.clients.client import BotClient
from programy.clients.restful.config import RestConfiguration

class RestBotClient(BotClient):
    __metaclass__ = ABCMeta

    def __init__(self, id, argument_parser=None):
        BotClient.__init__(self, id, argument_parser)
        self.api_keys = []

    def get_client_configuration(self):
        return RestConfiguration(self.id)

    def load_api_keys(self):
        if self.configuration.client_configuration.use_api_keys is True:
            if self.configuration.client_configuration.api_key_file is not None:
                try:
                    with open(self.configuration.client_configuration.api_key_file, "r", encoding="utf-8") as api_key_file:
                        for api_key in api_key_file:
                            self.api_keys.append(api_key.strip())

                except Exception as excep:
                    YLogger.exception(self, "Failed to open license key file [%s]", excep, self.configuration.client_configuration.api_key_file)

    def initialise(self):
        self.load_api_keys()

    @abstractmethod
    def get_api_key(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def get_question(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def get_userid(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def create_response(self, response, status):
        raise NotImplementedError()

    def is_apikey_valid(self, apikey):
        return bool(apikey in self.api_keys)

    def verify_api_key_usage(self, request):
        if self.configuration.client_configuration.use_api_keys is True:

            apikey = self.get_api_key(request)

            if apikey is None:
                YLogger.error(self, "Unauthorised access - api required but missing")
                return {'error': 'Unauthorized access'}, 401

            if self.is_apikey_valid(apikey) is False:
                YLogger.error(self, "'Unauthorised access - invalid api key")
                return {'error': 'Unauthorized access'}, 401

        return None, None

    def format_success_response(self, userid, question, answer):
        return {"question": question, "answer": answer, "userid": userid}

    def format_error_response(self, userid, question, error):
        client_context = self.create_client_context(userid)
        return {"question": question, "answer": client_context.bot.default_response, "userid": userid, "error": error}

    def ask_question(self, userid, question):
        response = ""
        try:
            self._questions += 1
            client_context = self.create_client_context(userid)
            response = client_context.bot.ask_question(client_context, question, responselogger=self)
        except Exception as e:
            print(e)
        return response

    def process_request(self, request):
        question = "Unknown"
        userid = "Unknown"
        try:
            response, status = self.verify_api_key_usage(request)
            if response is not None:
                return response, status

            question = self.get_question(request)
            userid = self.get_userid(request)

            answer = self.ask_question(userid, question)

            return self.format_success_response(userid, question, answer), 200

        except Exception as excep:

            return self.format_error_response(userid, question, str(excep)), 500
