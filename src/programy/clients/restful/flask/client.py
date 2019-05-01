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
from flask import Flask, jsonify, request, make_response, abort

from programy.clients.restful.client import RestBotClient


class FlaskRestBotClient(RestBotClient):

    def __init__(self, id, argument_parser=None):
        RestBotClient.__init__(self, id, argument_parser)
        self.initialise()

    def get_api_key(self, rest_request):
        if 'apikey' not in rest_request.args or rest_request.args['apikey'] is None:
            return None
        return rest_request.args['apikey']

    def server_abort(self, error_code):
        abort(error_code)

    def get_question(self, rest_request):
        if 'question' not in rest_request.args or rest_request.args['question'] is None:
            YLogger.error(self, "'question' missing from request")
            self.server_abort(400)
        return rest_request.args['question']

    def get_userid(self, rest_request):
        if 'userid' not in rest_request.args or rest_request.args['userid'] is None:
            YLogger.error(self, "'userid' missing from request")
            self.server_abort(400)
        return rest_request.args['userid']

    def create_response(self, response_data, status):
        if self.configuration.client_configuration.debug is True:
            self.dump_request(response_data)

        return make_response(jsonify({'response': response_data}, status))

    def run(self, flask):

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
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      ssl_context=context)
        else:
            print("%s Client running in http mode, careful now !" % self.id)
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug)

    def dump_request(self, request):
        YLogger.debug(self, str(request))


if __name__ == '__main__':

    REST_CLIENT = None

    print("Initiating Flask REST Service...")
    APP = Flask(__name__)

    @APP.route('/api/rest/v1.0/ask', methods=['GET'])
    def ask():
        response_data, status = REST_CLIENT.process_request(request)
        return REST_CLIENT.create_response(response_data, status)

    print("Loading, please wait...")
    REST_CLIENT = FlaskRestBotClient("flask")
    REST_CLIENT.run(APP)
