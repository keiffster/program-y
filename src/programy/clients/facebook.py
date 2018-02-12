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
import random
from flask import Flask, request
from pymessenger.bot import Bot

from programy.clients.client import BotClient
from programy.config.sections.client.facebook import FacebookConfiguration

FACEBOOK_CLIENT = None

class FacebookBotClient(BotClient):
    
    def __init__(self, argument_parser=None):
        BotClient.__init__(self, 'facebook', argument_parser)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Facebook Client is running....")

        self.get_license_keys()

        self._facebook_bot = self.create_facebook_bot()

        print("Facebook Client loaded")

    def get_license_keys(self):
        self._access_token = self.bot.license_keys.get_key("FACEBOOK_ACCESS_TOKEN")
        self._verify_token = self.bot.license_keys.get_key("FACEBOOK_VERIFY_TOKEN")

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Facebook")

    def get_client_configuration(self):
        return FacebookConfiguration()

    def ask_question(self, sessionid, question):
        response = self.bot.ask_question(sessionid, question, responselogger=self)
        return response

    def create_facebook_bot(self):
        return Bot(self._access_token)

    def verify_fb_token(self, token_sent):
        # take token sent by facebook and verify it matches the verify token you sent
        # if they match, allow the request, else return an error
        if token_sent == self._verify_token:
            return request.args.get("hub.challenge")
        return 'Invalid verification token'

    # uses PyMessenger to send response to user
    def send_message(self, recipient_id, response):
        # sends user the text message provided via input response parameter
        self._facebook_bot.send_text_message(recipient_id, response)
        return "success"

    def receive_message(self, request):
        if request.method == 'GET':
            """Before allowing people to message your bot, Facebook has implemented a verify token
            that confirms all requests that your bot receives came from Facebook."""
            token_sent = request.args.get("hub._verify_token")
            return self.verify_fb_token(token_sent)
        # if the request was not get, it must be POST and we can just proceed with sending a message back to user
        else:
            # get whatever message a user sent the bot
            output = request.get_json()
            for event in output['entry']:
                messaging = event['messaging']
                for message in messaging:
                    if message.get('message'):
                        # Facebook Messenger ID for user so we know where to send response back to
                        recipient_id = message['sender']['id']

                        # We have been send a text message, we can respond
                        if message['message'].get('text'):
                            response_sent_text = self.ask_question(recipient_id, message['message'].get('text'))
                            self.send_message(recipient_id, response_sent_text)

                        # else if user sends us a GIF, photo,video, or any other non-text item
                        elif message['message'].get('attachments'):
                            response_sent_nontext = "Sorry, I cannot handle attachements right now!"
                            self.send_message(recipient_id, response_sent_nontext)

                        # otherwise its a general error
                        else:
                            self.send_message(recipient_id, "Sorry, I do not understand you!")

        return "Message Processed"


APP = Flask(__name__)

#We will receive messages that Facebook sends our bot at this endpoint
@APP.route("/", methods=['GET', 'POST'])
def receive_message():
    try:
        return FACEBOOK_CLIENT.receive_message(request)
    except Exception as e:
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.exception(e)

if __name__ == "__main__":

    FACEBOOK_CLIENT = FacebookBotClient()

    print("Facebook Client running on %s:%s" % (FACEBOOK_CLIENT.configuration.client_configuration.host,
                                                FACEBOOK_CLIENT.configuration.client_configuration.port))

    if FACEBOOK_CLIENT.configuration.client_configuration.debug is True:
        print("Twilio Client running in debug mode")

    if FACEBOOK_CLIENT.configuration.client_configuration.ssl_cert_file is not None and \
            FACEBOOK_CLIENT.configuration.client_configuration.ssl_key_file is not None:
        context = (FACEBOOK_CLIENT.configuration.client_configuration.ssl_cert_file,
                   FACEBOOK_CLIENT.configuration.client_configuration.ssl_key_file)

        print("Facebook Client running in https mode")
        APP.run(host=FACEBOOK_CLIENT.configuration.client_configuration.host,
                port=FACEBOOK_CLIENT.configuration.client_configuration.port,
                debug=FACEBOOK_CLIENT.configuration.client_configuration.debug,
                ssl_context=context)
    else:
        print("Facebook Client running in http mode, careful now !")
        APP.run(host=FACEBOOK_CLIENT.configuration.client_configuration.host,
                port=FACEBOOK_CLIENT.configuration.client_configuration.port,
                debug=FACEBOOK_CLIENT.configuration.client_configuration.debug)
