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

#
# curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'
#


##############################################################
# IMPORTANT
# Sanic is not supported on windows due to a dependency on
# uvloop. This code will not run on Windows
#

import logging
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError

from programy.clients.rest import RestBotClient
from programy.bot import Bot

class SanicRestBotClient(RestBotClient):

    def __init__(self, argument_parser=None):
        RestBotClient.__init__(self, "SanicRest", argument_parser)

    def get_api_key(self, rest_request):
        if 'apikey' not in rest_request.raw_args or rest_request.raw_args['apikey'] is None:
            return None
        return rest_request.raw_args['apikey']

    def server_abort(self, message, status_code):
        raise ServerError(message, status_code=status_code)

    def get_question(self, rest_request):
        if 'question' not in rest_request.raw_args or rest_request.raw_args['question'] is None:
            print("'question' missing from rest_request")
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("'question' missing from rest_request")
            self.server_abort("'question' missing from rest_request", 500)
        return rest_request.raw_args['question']

    def get_sessionid(self, rest_request):
        if 'sessionid' not in rest_request.raw_args or rest_request.raw_args['sessionid'] is None:
            print("'sessionid' missing from rest_request")
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("'sessionid' missing from rest_request")
            self.server_abort("'sessionid' missing from rest_request", 500)
        return rest_request.raw_args['sessionid']

REST_CLIENT = None

print("Initiating REST Service...")
APP = Sanic()

@APP.route('/api/v1.0/ask', methods=['GET'])
async def ask(request):
    response, status = REST_CLIENT.process_request(request)
    return json(response, status=status)

if __name__ == '__main__':

    print("Loading, please wait...")
    REST_CLIENT = SanicRestBotClient()

    def run():

        print("REST Client running on %s:%s with %d workers" % (
            REST_CLIENT.configuration.client_configuration.host,
            REST_CLIENT.configuration.client_configuration.port,
            REST_CLIENT.configuration.client_configuration.workers))

        if REST_CLIENT.configuration.client_configuration.debug is True:
            print("REST Client running in debug mode")

        APP.run(host=REST_CLIENT.configuration.client_configuration.host,
                port=REST_CLIENT.configuration.client_configuration.port,
                debug=REST_CLIENT.configuration.client_configuration.debug,
                workers=REST_CLIENT.configuration.client_configuration.workers)

    run()
