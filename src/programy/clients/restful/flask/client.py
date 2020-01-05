"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from flask import Flask, jsonify, request, make_response, abort, Response

from programy.clients.restful.client import RestBotClient
from programy.utils.console.console import outputLog


class FlaskRestBotClient(RestBotClient):

    def __init__(self, botid, argument_parser=None):
        RestBotClient.__init__(self, botid, argument_parser)
        self.initialise()

    def _render_callback(self):
        return False

    def server_abort(self, message, status_code):
        abort(Response(message), status_code)

    def make_response_v1(self, data, status_code):
        return make_response(jsonify(data, status_code))

    def make_response_v2(self, data, status_code):
        return make_response(jsonify(data), status_code)

    def make_response_other(self, data, status_code):
        return make_response(data, status_code)

    def create_response(self, response_data, status_code, version=1.0):
        if self.configuration.client_configuration.debug is True:
            self.dump_request(response_data)

        if version == 1.0:
            return self.make_response_v1(response_data, status_code)
        elif version == 2.0:
            return self.make_response_v2(response_data, status_code)

        return self.make_response_other('Invalid API version', 400)

    def run(self, app=None):

        outputLog(self, "%s Client running on http://%s:%s" % (self.id, self.configuration.client_configuration.host,
                                                               self.configuration.client_configuration.port))

        self.startup()

        if self.configuration.client_configuration.debug is True:
            outputLog(self, "%s Client running in debug mode" % self.id)

        if self.configuration.client_configuration.ssl_cert_file is not None and \
                self.configuration.client_configuration.ssl_key_file is not None:
            context = (self.configuration.client_configuration.ssl_cert_file,
                       self.configuration.client_configuration.ssl_key_file)

            outputLog(self, "%s Client running in https mode" % self.id)
            app.run(host=self.configuration.client_configuration.host,
                    port=self.configuration.client_configuration.port,
                    debug=self.configuration.client_configuration.debug,
                    ssl_context=context)
        else:
            outputLog(self, "%s Client running in http mode, careful now !" % self.id)
            app.run(host=self.configuration.client_configuration.host,
                    port=self.configuration.client_configuration.port,
                    debug=self.configuration.client_configuration.debug)

        self.shutdown()


if __name__ == '__main__':
    REST_CLIENT = None

    outputLog(None, "Initiating Flask REST Service...")
    APP = Flask(__name__)


    @APP.route('/api/rest/v1.0/ask', methods=['GET', 'POST'])
    def ask_v1_0():
        response_data, status = REST_CLIENT.process_request(request, version=1.0)
        return REST_CLIENT.create_response(response_data, status, version=1.0)


    @APP.route('/api/rest/v2.0/ask', methods=['GET', 'POST'])
    def ask_v2_0():
        response_data, status = REST_CLIENT.process_request(request, version=2.0)
        return REST_CLIENT.create_response(response_data, status, version=2.0)


    outputLog(None, "Loading, please wait...")
    REST_CLIENT = FlaskRestBotClient("flask")
    REST_CLIENT.run(APP)
