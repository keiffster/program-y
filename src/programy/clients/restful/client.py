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
from programy.clients.restful.apihandlers import APIHandler_V1_0, APIHandler_V2_0


class RestBotClient(BotClient):
    __metaclass__ = ABCMeta

    def __init__(self, id, argument_parser=None):
        BotClient.__init__(self, id, argument_parser)
        self.api_keys = []
        self._v1_0_handler = APIHandler_V1_0(self)
        self._v2_0_handler = APIHandler_V2_0(self)

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

    def get_api_key(self, rest_request):
        if 'apikey' not in rest_request.args or rest_request.args['apikey'] is None:
            return None
        return rest_request.args['apikey']

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

    def get_variable(self, rest_request, name, method='GET'):
        if method == 'GET':
            if name not in rest_request.args or rest_request.args[name] is None:
                YLogger.error(self, "'%s' missing from GET request", name)
                self.server_abort(400)
            return rest_request.args[name]

        elif method == 'POST':
            if name not in rest_request.json or rest_request.json[name] is None:
                YLogger.error(self, "'%s' missing from POST request", name)
                self.server_abort(400)
            return rest_request.json[name]

        else:
            YLogger.error(self, "Invalid REST request type '%s'", method)
            self.server_abort(400)

    @abstractmethod
    def server_abort(self, error_code):
        raise NotImplementedError()

    @abstractmethod
    def create_response(self, response, status):
        raise NotImplementedError()

    def _get_metadata(self, client_context, metadata):

        if client_context.brain.properties.has_property("fullname"):
            metadata['botName'] = client_context.brain.properties.property("fullname")
        else:
            metadata['botName'] = "Program-y"

        if client_context.brain.properties.has_property("app_version"):
            metadata['version'] = client_context.brain.properties.property("app_version")
        else:
            metadata['version'] = "1.0.0"

        if client_context.brain.properties.has_property("copyright"):
            metadata['copyright'] = client_context.brain.properties.property("copyright")
        else:
            metadata['copyright'] = "Copyright 2016-2019 keithsterling.com"

        if client_context.brain.properties.has_property("botmaster"):
            metadata['authors'] = [client_context.brain.properties.property("botmaster")]
        else:
            metadata['authors'] = ["Keith Sterling"]

    def ask_question(self, userid, question, metadata=None):
        response = ""
        try:
            self._questions += 1
            client_context = self.create_client_context(userid)
            response = client_context.bot.ask_question(client_context, question, responselogger=self)

            if metadata is not None:
                self._get_metadata(client_context, metadata)

        except Exception as e:
            YLogger.exception_nostack(self, "Failed to ask question", e)

        return response

    def process_v1_0_request(self, request):
        return self._v1_0_handler.process_request(request)

    def process_v2_0_request(self, request):
        return self._v2_0_handler.process_request(request)

    def dump_request(self, request):
        YLogger.debug(self, str(request))
