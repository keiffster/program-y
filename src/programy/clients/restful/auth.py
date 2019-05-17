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


class RestBasicAuthorizationHandler(RestAuthorizationHandler):

    BASIC = "Basic"

    def __init__(self, configuration: RestConfiguration):
        RestAuthorizationHandler.__init__(self, configuration)

    @staticmethod
    def get_license_key(client):
        return client.license_keys.get_key("BASIC_AUTH_TOKEN")

    def initialise(self, client):
        self._basic_auth_token = self.get_license_key(client)

    def authorise(self, request):
        if 'Authorization' in request.headers:
            authorization = request.headers['Authorization']
            parts = authorization.split(" ")
            if len(parts) > 1:
                type = parts[0].strip()
                if type == RestBasicAuthorizationHandler.BASIC:
                    token = " ".join(parts[1:])
                    if token == self._basic_auth_token:
                        return True

        return False
