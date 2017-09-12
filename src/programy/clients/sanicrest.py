"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

#
# curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'
#

import logging
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError

from programy.clients.rest import RestBotClient

class SanicRestBotClient(RestBotClient):

    def __init__(self, argument_parser=None):
        self.clientid = "Rest"
        RestBotClient.__init__(self, argument_parser)

    def get_api_key(self, request):
        if 'apikey' not in request.raw_args or request.raw_args['apikey'] is None:
            return None
        else:
            return request.raw_args['apikey']

    def server_abort(self, message, status_code):
        raise ServerError(message, status_code=status_code)

    def get_question(self, request):
        if 'question' not in request.raw_args or request.raw_args['question'] is None:
            print("'question' missing from request")
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'question' missing from request")
            self.server_abort("'question' missing from request", 500)
        return request.raw_args['question']

    def get_sessionid(self, request):
        if 'sessionid' not in request.raw_args or request.raw_args['sessionid'] is None:
            print("'sessionid' missing from request")
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'sessionid' missing from request")
            self.server_abort("'sessionid' missing from request", 500)
        return request.raw_args['sessionid']

rest_client = None

print("Initiating REST Service...")
app = Sanic()

@app.route('/api/v1.0/ask', methods=['GET'])
async def ask(request):
    global rest_client
    response, status = rest_client.process_request(request)
    return json(response, status=status)

if __name__ == '__main__':

    print("Loading, please wait...")
    rest_client = SanicRestBotClient()

    def run():

        global rest_client

        print("REST Client running on %s:%s" % (rest_client.configuration.client_configuration.host,
                                                rest_client.configuration.client_configuration.port))

        if rest_client.configuration.client_configuration.debug is True:
            print("REST Client running in debug mode")

        app.run(host=rest_client.configuration.client_configuration.host,
                port=rest_client.configuration.client_configuration.port,
                debug=rest_client.configuration.client_configuration.debug,
                workers=rest_client.configuration.client_configuration.workers)

    run()
