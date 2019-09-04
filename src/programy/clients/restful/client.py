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
from programy.clients.restful.apikeys import APIKeysHandler
from programy.clients.restful.auth import RestAuthorizationHandler


class RestBotClient(BotClient):
    __metaclass__ = ABCMeta

    def __init__(self, id, argument_parser=None):
        BotClient.__init__(self, id, argument_parser)
        self._api_keys = APIKeysHandler(self.configuration.client_configuration)
        self._authorization = None
        self._v1_0_handler = APIHandler_V1_0(self)
        self._v2_0_handler = APIHandler_V2_0(self)

    @property
    def api_keys(self):
        return self._api_keys

    def get_client_configuration(self):
        return RestConfiguration(self.id)

    def initialise(self):
        self._api_keys.load_api_keys()
        self._authorization = RestAuthorizationHandler.load_authorisation(self)

    def get_variable(self, rest_request, name, method='GET'):
        if method == 'GET':
            if name not in rest_request.args or rest_request.args[name] is None:
                YLogger.error(self, "'%s' missing from GET request", name)
                self.server_abort(message="'%s' missing from GET request"%name, status_code=400)
            return rest_request.args[name]

        elif method == 'POST':
            if name not in rest_request.json or rest_request.json[name] is None:
                YLogger.error(self, "'%s' missing from POST request", name)
                self.server_abort(message="'%s' missing from POST request"%name, status_code=400)
            return rest_request.json[name]

        else:
            YLogger.error(self, "Invalid REST request type '%s'", method)
            self.server_abort(message="Invalid REST request type '%s'"%method, status_code=400)

    @abstractmethod
    def server_abort(self, message, status_code):
        raise NotImplementedError()

    @abstractmethod
    def create_response(self, response_data, status_code, version=1.0):
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

    def process_request(self, request, version=1.0):

        if self._authorization is not None:
            if self._authorization.authorise(request) is False:
                return "Access denied", 403

        if self._api_keys is not None:
            if self._api_keys.use_api_keys():
                if self._api_keys.verify_api_key_usage(request) is False:
                    return 'Unauthorized access', 401

        if version == 1.0:
            return self._v1_0_handler.process_request(request)

        elif version == 2.0:
            return self._v2_0_handler.process_request(request)

        else:
            return 'Invalid API version', 400

    def dump_request(self, request):
        YLogger.debug(self, str(request))
