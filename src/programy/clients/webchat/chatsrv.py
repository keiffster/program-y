import logging

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import abort
from flask import current_app
from programy.clients.client import BotClient
from programy.config.sections.client.webchat import WebChatConfiguration

class WebChatBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self, "WebChat")

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "REST")

    def get_client_configuration(self):
        return WebChatConfiguration()

print("Loading, please wait...")
WEBCHAT_CLIENT = WebChatBotClient()

print("Initiating Webchat Client...")
APP = Flask(__name__)

@APP.route('/')
def index():
    return current_app.send_static_file('webchat.html')

# Enter you API keys, here, alternatively store in a db or file and load at startup
# This is an exmaple, and therefore not suitable for production
API_KEYS = [
]

def is_apikey_valid(apikey):
    return bool(apikey in API_KEYS)

@APP.route('/api/v1.0/ask', methods=['GET'])
def ask():

    if WEBCHAT_CLIENT.configuration.client_configuration.use_api_keys is True:
        if 'apikey' not in request.args or request.args['apikey'] is None:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Unauthorised access - api required but missing")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

        apikey = request.args['apikey']
        if is_apikey_valid(apikey) is False:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("'Unauthorised access - invalid api key")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    if 'question' not in request.args or request.args['question'] is None:
        print("'question' missing from request")
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.error("'question' missing from request")
        abort(400)

    question = request.args['question']

    if 'sessionid' not in request.args or request.args['sessionid'] is None:
        print("'sessionid' missing from request")
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.error("'sessionid' missing from request")
        abort(400)

    sessionid = request.args['sessionid']

    try:
        answer = WEBCHAT_CLIENT.bot.ask_question(sessionid, question, responselogger=WEBCHAT_CLIENT)

        response = {"question": question,
                    "answer": answer,
                    "sessionid": sessionid
                   }

        return jsonify({'response': response})

    except Exception as excep:
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.exception(excep)

        response = {"question": question,
                    "answer": WEBCHAT_CLIENT.bot.default_response,
                    "sessionid": sessionid,
                    "error": str(excep)
                   }

        return jsonify({'response': response})

if __name__ == '__main__':

    import signal
    import sys

    def set_exit_handler(func):
        signal.signal(signal.SIGTERM, func)

    def on_exit(sig, func=None):
        print("exit handler triggered")
        sys.exit(1)

    def run():
        print("WebChat Client running on %s:%s" % (WEBCHAT_CLIENT.configuration.client_configuration.host,
                                                   WEBCHAT_CLIENT.configuration.client_configuration.port))
        if WEBCHAT_CLIENT.configuration.client_configuration.debug is True:
            print("WebChat Client running in debug mode")

        APP.run(host=WEBCHAT_CLIENT.configuration.client_configuration.host,
                port=WEBCHAT_CLIENT.configuration.client_configuration.port,
                debug=WEBCHAT_CLIENT.configuration.client_configuration.debug)


    set_exit_handler(on_exit)

    run()
