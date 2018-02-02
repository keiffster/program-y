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
from flask import Flask, jsonify, request, make_response, abort

from programy.clients.rest import RestBotClient

class FlaskRestBotClient(RestBotClient):

    def __init__(self, argument_parser=None):
        RestBotClient.__init__(self, "FlaskRest", argument_parser)
        self.initialise()

    def get_api_key(self, rest_request):
        if 'apikey' not in rest_request.args or rest_request.args['apikey'] is None:
            return None
        return rest_request.args['apikey']

    def server_abort(self, error_code):
        abort(error_code)

    def get_question(self, rest_request):
        if 'question' not in rest_request.args or rest_request.args['question'] is None:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("'question' missing from request")
            self.server_abort(400)
        return rest_request.args['question']

    def get_sessionid(self, rest_request):
        if 'sessionid' not in rest_request.args or rest_request.args['sessionid'] is None:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("'sessionid' missing from request")
            self.server_abort(400)
        return rest_request.args['sessionid']

REST_CLIENT = None

print("Initiating REST Service...")
APP = Flask(__name__)

@APP.route('/api/v1.0/ask', methods=['GET'])
def ask():
    response, status = REST_CLIENT.process_request(request)
    return make_response(jsonify({'response': response}, status))

if __name__ == '__main__':

    print("Loading, please wait...")
    REST_CLIENT = FlaskRestBotClient()

    def run():

        print("REST Client running on %s:%s" % (REST_CLIENT.configuration.client_configuration.host,
                                                REST_CLIENT.configuration.client_configuration.port))

        if REST_CLIENT.configuration.client_configuration.debug is True:
            print("REST Client running in debug mode")

        if REST_CLIENT.configuration.client_configuration.ssl_cert_file is not None and \
           REST_CLIENT.configuration.client_configuration.ssl_key_file is not None:
            context = (REST_CLIENT.configuration.client_configuration.ssl_cert_file,
                       REST_CLIENT.configuration.client_configuration.ssl_key_file)

            print("REST Client running in https mode")
            APP.run(host=REST_CLIENT.configuration.client_configuration.host,
                    port=REST_CLIENT.configuration.client_configuration.port,
                    debug=REST_CLIENT.configuration.client_configuration.debug,
                    ssl_context=context)
        else:
            print("REST Client running in http mode, careful now !")
            APP.run(host=REST_CLIENT.configuration.client_configuration.host,
                    port=REST_CLIENT.configuration.client_configuration.port,
                    debug=REST_CLIENT.configuration.client_configuration.debug)

    run()
