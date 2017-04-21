import logging
import time
from flask import Flask, request

from fbmessenger import BaseMessenger

from programy.clients.clients import BotClient
from programy.config.client.facebook import FacebookClientConfiguration

# This uses https://ngrok.com/ to create a secure tunnel to localhost
# Required by facebook to send message notifications

# https://github.com/rehabstudio/fbmessenger/tree/master/example

class FacebookMessenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(FacebookMessenger, self).__init__(self.page_access_token)

    def message(self, message):
        self.send({'text': 'Received: {0}'.format(message['message']['text'])})

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        pass

    def optin(self, message):
        pass


class FacebookBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "Facebook"])

    def get_client_configuration(self):
        return FacebookClientConfiguration()

    def run(self):

        self._page_token = self.bot.license_keys.get_key("FACEBOOK_PAGE_TOKEN")
        self._verify_token = self.bot.license_keys.get_key("FACEBOOK_VERIFY_TOKEN")

        self._messenger = FacebookMessenger(self._page_token)

app = Flask(__name__)
app.debug = True

twitter_app = FacebookBotClient()
twitter_app.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("Hello")
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == twitter_app._verify_token:
            #return request.args.get('hub.challenge')
            return 'OK'
        raise ValueError('FACEBOOK_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        twitter_app._messenger.handle(request.get_json(force=True))
    return ''

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)

