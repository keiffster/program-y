"""
Copyright (c) 2016 Keith Sterling

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
from flask import Flask, jsonify, request, make_response, abort

from programy.clients.clients import BotClient
from programy.config import RestClientConfiguration

class RestBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "REST"])

    def get_client_configuration(self):
        return RestClientConfiguration()

print("Loading, please wait...")
rest_client = RestBotClient()

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

@app.route('/api/v1.0/ask', methods=['GET'])
def ask():

    if rest_client.configuration.rest_configuration._use_api_keys:
        if 'apikey' not in request.args or request.args['apikey'] is None:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    apikey = request.args['apikey']
    if is_apikey_valid(apikey) is False:
        return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    if 'question' not in request.args or request.args['question'] is None:
        abort(400)

    question  = request.args['question']

    if 'sessionid' not in request.args or request.args['sessionid'] is None:
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

    except Exception as e:
        print(e)

        response = {"question": question,
                    "answer": rest_client.bot.default_response,
                    "sessionid": sessionid
                    }

        return jsonify({'response': response}, 400)

if __name__ == '__main__':

    print("REST Client running on %s:%s" % (rest_client.configuration.rest_configuration.host, rest_client.configuration.rest_configuration.port))
    if rest_client.configuration.rest_configuration.debug is True:
        print("REST Client running in debug mode")

    app.run(host=rest_client.configuration.rest_configuration.host,
            port=rest_client.configuration.rest_configuration.port,
            debug=rest_client.configuration.rest_configuration.debug)