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

# https://www.twilio.com/docs/quickstart/python/sms#sign-up-for-twilio-and-get-a-phone-number

import logging

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from programy.clients.client import BotClient
from programy.config.sections.client.twilio import TwilioConfiguration

TWILIO_CLIENT = None

class TwilioBotClient(BotClient):
    
    def __init__(self, argument_parser=None):
        BotClient.__init__(self, 'twilio', argument_parser)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Twilio Client is running....")

        self.get_license_keys()

        self._twilio_client = self.create_twilio_client()

        print("Twilio Client loaded")

    @property
    def from_number(self):
        return self._from_number

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Twilio")

    def get_license_keys(self):
        self._account_sid = self.bot.license_keys.get_key("TWILIO_ACCOUNT_SID")
        self._auth_token = self.bot.license_keys.get_key("TWILIO_AUTH_TOKEN")
        self._from_number = self.bot.license_keys.get_key("TWILIO_FROM_NUMBER")

    def get_client_configuration(self):
        return TwilioConfiguration()

    def create_twilio_client(self):
        return Client(self._account_sid, self._auth_token)

    def ask_question(self, sessionid, question):
        response = self.bot.ask_question(sessionid, question, responselogger=self)
        return response

    def create_response(self, client_number, answer):
        response = MessagingResponse()
        response.message(body=answer, to=client_number)
        response_str = str(response)
        return response_str

    def receive_message(self, request):
        if request.method == 'POST':
            client_number = request.form['From']
            question = request.form['Body']
        else:
            client_number = request.args.get('From')
            question = request.args.get('Body')

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Twillio received [%s] from [%s]"%(question, client_number))

        answer = self.ask_question(client_number, question)

        response = self.create_response(client_number, answer)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Twillio sending [%s] to [%s]"%(answer, client_number))

        return response

APP = Flask(__name__)

#We will receive messages that Twilio sends our bot at this endpoint
@APP.route("/sms", methods=['POST'])
def receive_message():
    try:
        return TWILIO_CLIENT.receive_message(request)
    except Exception as e:
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.exception(e)
        return ""

if __name__ == "__main__":

    TWILIO_CLIENT = TwilioBotClient()

    print("Twilio Client running on %s:%s, receiving on %s" % (TWILIO_CLIENT.configuration.client_configuration.host,
                                                             TWILIO_CLIENT.configuration.client_configuration.port,
                                                             TWILIO_CLIENT.from_number))


    if TWILIO_CLIENT.configuration.client_configuration.debug is True:
        print("Twilio Client running in debug mode")

    if TWILIO_CLIENT.configuration.client_configuration.ssl_cert_file is not None and \
            TWILIO_CLIENT.configuration.client_configuration.ssl_key_file is not None:
        context = (TWILIO_CLIENT.configuration.client_configuration.ssl_cert_file,
                   TWILIO_CLIENT.configuration.client_configuration.ssl_key_file)

        print("Twilio Client running in https mode")
        APP.run(host=TWILIO_CLIENT.configuration.client_configuration.host,
                port=TWILIO_CLIENT.configuration.client_configuration.port,
                debug=TWILIO_CLIENT.configuration.client_configuration.debug,
                ssl_context=context)
    else:
        print("Twilio Client running in http mode, careful now !")
        APP.run(host=TWILIO_CLIENT.configuration.client_configuration.host,
                port=TWILIO_CLIENT.configuration.client_configuration.port,
                debug=TWILIO_CLIENT.configuration.client_configuration.debug)

