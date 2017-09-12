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

import logging
from flask import Flask, jsonify, request, make_response, abort

from programy.clients.rest import RestBotClient

class FlaskRestBotClient(RestBotClient):

    def __init__(self, argument_parser=None):
        self.clientid = "Rest"
        RestBotClient.__init__(self, argument_parser)
        self.initialise()

    def get_api_key(self, request):
        if 'apikey' not in request.args or request.args['apikey'] is None:
            return None
        else:
            return request.args['apikey']

    def server_abort(self, error_code):
        abort(error_code)

    def get_question(self, request):
        if 'question' not in request.args or request.args['question'] is None:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'question' missing from request")
            self.server_abort(400)
        return request.args['question']

    def get_sessionid(self, request):
        if 'sessionid' not in request.args or request.args['sessionid'] is None:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'sessionid' missing from request")
            self.server_abort(400)
        return request.args['sessionid']

rest_client = None

print("Initiating REST Service...")
app = Flask(__name__)

@app.route('/api/v1.0/ask', methods=['GET'])
def ask():
    global rest_client
    response, status = rest_client.process_request(request)
    return make_response(jsonify({'response': response}, status))

if __name__ == '__main__':

    print("Loading, please wait...")
    rest_client = FlaskRestBotClient()

    def run():
        global rest_client

        print("REST Client running on %s:%s" % (rest_client.configuration.client_configuration.host,
                                                rest_client.configuration.client_configuration.port))

        if rest_client.configuration.client_configuration.debug is True:
            print("REST Client running in debug mode")

        app.run(host=rest_client.configuration.client_configuration.host,
                port=rest_client.configuration.client_configuration.port,
                debug=rest_client.configuration.client_configuration.debug)

    run()
