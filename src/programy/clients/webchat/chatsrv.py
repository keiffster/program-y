import logging

from flask import Flask, jsonify, request, make_response, abort, current_app
from programy.clients.client import BotClient
from programy.config.sections.client.webchat import WebChatConfiguration

class WebChatBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "REST")

    def get_client_configuration(self):
        return WebChatConfiguration()

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

    if webchat_client.configuration.client_configuration.use_api_keys is True:
        if 'apikey' not in request.args or request.args['apikey'] is None:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Unauthorised access - api required but missing")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

        apikey = request.args['apikey']
        if is_apikey_valid(apikey) is False:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'Unauthorised access - invalid api key")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    if 'question' not in request.args or request.args['question'] is None:
        print("'question' missing from request")
        if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'question' missing from request")
        abort(400)

    question = request.args['question']

    if 'sessionid' not in request.args or request.args['sessionid'] is None:
        print("'sessionid' missing from request")
        if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'sessionid' missing from request")
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

    import os, signal, sys

    def set_exit_handler(func):
        signal.signal(signal.SIGTERM, func)

    def on_exit(sig, func=None):
        print("exit handler triggered")
        sys.exit(1)

    def run():
        print("WebChat Client running on %s:%s" % (webchat_client.configuration.client_configuration.host,
                                                   webchat_client.configuration.client_configuration.port))
        if webchat_client.configuration.client_configuration.debug is True:
            print("WebChat Client running in debug mode")

        app.run(host=webchat_client.configuration.client_configuration.host,
                port=webchat_client.configuration.client_configuration.port,
                debug=webchat_client.configuration.client_configuration.debug)


    set_exit_handler(on_exit)

    run()
