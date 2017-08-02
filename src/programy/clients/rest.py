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

from programy.clients.client import BotClient
from programy.config.sections.client.rest import RestConfiguration

class RestBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, argument_parser)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "REST"])

    def get_client_configuration(self):
        return RestConfiguration()

rest_client = None

print("Initiating REST Service...")
app = Flask(__name__)

# Enter you API keys, here, alternatively store in a db or file and load at startup
# This is an exmaple, and therefore not suitable for production
api_keys = [
]

def is_apikey_valid(apikey):
    if apikey in api_keys:
        return True
    else:
        return False

# Example Usage
#
# curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'
#
@app.route('/api/v1.0/ask', methods=['GET'])
def ask():

    if rest_client.configuration.client_configuration.use_api_keys is True:
        if 'apikey' not in request.args or request.args['apikey'] is None:
            logging.error("Unauthorised access - api required but missing")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

        apikey = request.args['apikey']
        if is_apikey_valid(apikey) is False:
            logging.error("'Unauthorised access - invalid api key")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    if 'question' not in request.args or request.args['question'] is None:
        print("'question' missing from request")
        logging.error("'question' missing from request")
        abort(400)

    question = request.args['question']

    if 'sessionid' not in request.args or request.args['sessionid'] is None:
        print("'sessionid' missing from request")
        logging.error("'sessionid' missing from request")
        abort(400)

    sessionid = request.args['sessionid']

    try:
        response = rest_client.bot.ask_question(sessionid, question)
        if response is None:
            answer = rest_client.bot.default_response
            rest_client.log_unknown_response(question)
        else:
            answer = response
            rest_client.log_response(question, response)

        response = {"question": question,
                    "answer": answer,
                    "sessionid": sessionid
                   }

        return jsonify({'response': response})

    except Exception as excep:

        response = {"question": question,
                    "answer": rest_client.bot.default_response,
                    "sessionid": sessionid,
                    "error": str(excep)
                   }

        return jsonify({'response': response})

if __name__ == '__main__':

    print("Loading, please wait...")
    rest_client = RestBotClient()

    def run():

        print("REST Client running on %s:%s" % (rest_client.configuration.client_configuration.host,
                                                rest_client.configuration.client_configuration.port))

        if rest_client.configuration.client_configuration.debug is True:
            print("REST Client running in debug mode")

        app.run(host=rest_client.configuration.client_configuration.host,
                port=rest_client.configuration.client_configuration.port,
                debug=rest_client.configuration.client_configuration.debug)

    run()
