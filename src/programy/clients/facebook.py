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

"""
Current commented out so that I do  not have to include fbmessenger in the list of dependencies

from flask import Flask, request

from fbmessenger import BaseMessenger

from programy.clients.client import BotClient
from programy.config.sections.client.facebook import FacebookConfiguration

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

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, argument_parser)

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "Facebook"])

    def get_client_configuration(self):
        return FacebookConfiguration()

    def run(self):

        self._page_token = self.bot.license_keys.get_key("FACEBOOK_PAGE_TOKEN")
        self._verify_token = self.bot.license_keys.get_key("FACEBOOK_VERIFY_TOKEN")

        self._messenger = FacebookMessenger(self._page_token)

app = Flask(__name__)
app.debug = True

facebook_app = None

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("Hello")
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == facebook_app._verify_token:
            #return request.args.get('hub.challenge')
            return 'OK'
        raise ValueError('FACEBOOK_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        facebook_app._messenger.handle(request.get_json(force=True))
    return ''

if __name__ == '__main__':

    facebook_app = FacebookBotClient()
    print("App running on http://127.0.0.0:8080")
    app.run(host='127.0.0.1', port=8080, debug=False)

"""