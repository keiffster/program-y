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

#
# curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&userid=1234567890'
#


##############################################################
# IMPORTANT
# Sanic is not supported on windows due to a dependency on
# uvloop. This code will not run on Windows
#

from programy.utils.logging.ylogger import YLogger
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError

from programy.clients.restful.client import RestBotClient
from programy.clients.restful.sanic.config import SanicRestConfiguration

class SanicRestBotClient(RestBotClient):

    def __init__(self, id, argument_parser=None):
        RestBotClient.__init__(self, id, argument_parser)

    def get_client_configuration(self):
        return SanicRestConfiguration("rest")

    def get_api_key(self, rest_request):
        if 'apikey' not in rest_request.raw_args or rest_request.raw_args['apikey'] is None:
            return None
        return rest_request.raw_args['apikey']

    def server_abort(self, message, status_code):
        raise ServerError(message, status_code=status_code)

    def get_question(self, rest_request):
        if 'question' not in rest_request.raw_args or rest_request.raw_args['question'] is None:
            YLogger.error(self, "'question' missing from rest_request")
            self.server_abort("'question' missing from rest_request", 500)
        return rest_request.raw_args['question']

    def get_userid(self, rest_request):
        if 'userid' not in rest_request.raw_args or rest_request.raw_args['userid'] is None:
            YLogger.error(self, "'userid' missing from rest_request")
            self.server_abort("'userid' missing from rest_request", 500)
        return rest_request.raw_args['userid']

    def create_response(self, response, status):
        return json(response, status=status)

    def run(self, sanic):

        print("%s Client running on %s:%s" % (self.id, self.configuration.client_configuration.host,
                                              self.configuration.client_configuration.port))

        self.startup()

        if self.configuration.client_configuration.debug is True:
            print("%s Client running in debug mode" % self.id)

        if self.configuration.client_configuration.ssl_cert_file is not None and \
                self.configuration.client_configuration.ssl_key_file is not None:
            context = (self.configuration.client_configuration.ssl_cert_file,
                       self.configuration.client_configuration.ssl_key_file)

            print("%s Client running in https mode" % self.id)
            sanic.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      ssl_context=context)
        else:
            print("%s Client running in http mode, careful now !" % self.id)
            sanic.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      workers = self.configuration.client_configuration.workers)

        self.shutdown()

    def dump_request(self, request):
        pass


if __name__ == '__main__':

    REST_CLIENT = None

    print("Initiating Sanic REST Service...")

    APP = Sanic()

    @APP.route('/api/rest/v1.0/ask', methods=['GET'])
    async def ask(request):
        response, status = REST_CLIENT.process_request(request)
        return REST_CLIENT.create_response(response, status=status)

    print("Loading, please wait...")
    REST_CLIENT = SanicRestBotClient("sanic")
    REST_CLIENT.run(APP)
