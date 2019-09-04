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
from programy.clients.restful.config import RestConfiguration


class RestAuthorizationHandler(object):

    AUTHORIZATION = "Authorization"

    def __init__(self, configuration: RestConfiguration):
        self._configuration = configuration

    def initialise(self, client):
        pass

    @staticmethod
    def load_authorisation(client):
        if client.configuration.client_configuration.authorization is not None:
            if client.configuration.client_configuration.authorization == 'Basic':
                YLogger.info(client, "Loading Authorization - Basic")
                auth = RestBasicAuthorizationHandler(client.configuration.client_configuration)
                auth.initialise(client)
                return auth
            else:
                YLogger.error(client, "Unsupported Authentication [%s]", client.configuration.client_configuration.authorization)
        return None


class RestBasicAuthorizationHandler(RestAuthorizationHandler):

    BASIC = "Basic"
    BASIC_AUTH_TOKEN = 'BASIC_AUTH_TOKEN'

    def __init__(self, configuration: RestConfiguration):
        RestAuthorizationHandler.__init__(self, configuration)
        self._basic_auth_token = None

    @staticmethod
    def get_auth_token_from_license_keys(client_context):
        return client_context.client.license_keys.get_key(RestBasicAuthorizationHandler.BASIC_AUTH_TOKEN)

    @staticmethod
    def add_authorisation_header(client_context, headers):
        headers[RestBasicAuthorizationHandler.AUTHORIZATION] = "Basic %s" % \
                            client_context.client.license_keys.get_key(RestBasicAuthorizationHandler.BASIC_AUTH_TOKEN)

    @staticmethod
    def get_license_key(client):
        return client.license_keys.get_key(RestBasicAuthorizationHandler.BASIC_AUTH_TOKEN)

    def initialise(self, client):
        self._basic_auth_token = RestBasicAuthorizationHandler.get_license_key(client)

    def authorise(self, request):
        if RestBasicAuthorizationHandler.AUTHORIZATION in request.headers:
            authorization = request.headers[RestBasicAuthorizationHandler.AUTHORIZATION]
            parts = authorization.split(" ")
            if len(parts) > 1:
                type = parts[0].strip()
                if type == RestBasicAuthorizationHandler.BASIC:
                    token = " ".join(parts[1:])
                    if token == self._basic_auth_token:
                        return True

        return False

