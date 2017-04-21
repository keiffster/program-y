import logging

from flask import Flask, jsonify, request, make_response, abort, current_app
from programy.clients.clients import BotClient
from programy.config.client.webchat import WebChatClientConfiguration

class WebChatBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "REST"])

    def get_client_configuration(self):
        return WebChatClientConfiguration()

print("Loading, please wait...")
webchat_client = WebChatBotClient()

print("Initiating Webchat Client...")
app = Flask(__name__)

@app.route('/')
def hello_world():
    return current_app.send_static_file('webchat.html')

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

    if webchat_client.configuration.webchat_configuration.use_api_keys is True:
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
        response = webchat_client.bot.ask_question(sessionid, question)
        if response is None:
            answer = webchat_client.bot.default_response
            webchat_client.log_unknown_response(question)
        else:
            answer = response
            webchat_client.log_response(question, response)

        response = {"question": question,
                    "answer": answer,
                    "sessionid": sessionid
                   }

        return jsonify({'response': response})

    except Exception as excep:

        response = {"question": question,
                    "answer": webchat_client.bot.default_response,
                    "sessionid": sessionid,
                    "error": str(excep)
                   }

        return jsonify({'response': response})

if __name__ == '__main__':

    def run():
        print("REST Client running on %s:%s" % (webchat_client.configuration.webchat_configuration.host,
                                                webchat_client.configuration.webchat_configuration.port))
        if webchat_client.configuration.webchat_configuration.debug is True:
            print("REST Client running in debug mode")

        app.run(host=webchat_client.configuration.webchat_configuration.host,
                port=webchat_client.configuration.webchat_configuration.port,
                debug=webchat_client.configuration.webchat_configuration.debug)

    run()
