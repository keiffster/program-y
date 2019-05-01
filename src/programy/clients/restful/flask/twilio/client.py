"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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

from programy.utils.logging.ylogger import YLogger

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.twilio.config import TwilioConfiguration

TWILIO_CLIENT = None

class TwilioBotClient(FlaskRestBotClient):
    
    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, 'twilio', argument_parser)

        YLogger.debug(self, "Twilio Client is running....")

        self.get_license_keys()

        self._twilio_client = self.create_twilio_client()

        print("Twilio Client loaded")

    @property
    def from_number(self):
        return self._from_number

    def get_license_keys(self):
        self._account_sid = self.license_keys.get_key("TWILIO_ACCOUNT_SID")
        self._auth_token = self.license_keys.get_key("TWILIO_AUTH_TOKEN")
        self._from_number = self.license_keys.get_key("TWILIO_FROM_NUMBER")

    def get_client_configuration(self):
        return TwilioConfiguration()

    def create_twilio_client(self):
        return Client(self._account_sid, self._auth_token)

    def create_response(self, client_number, answer):
        response = MessagingResponse()
        response.message(body=answer, to=client_number)
        response_str = str(response)
        return response_str

    def receive_message(self, request):

        if self.configuration.client_configuration.debug is True:
            self.dump_request(request)

        if request.method == 'POST':
            client_number = request.form['From']
            question = request.form['Body']
        else:
            client_number = request.args.get('From')
            question = request.args.get('Body')

        YLogger.debug(self, "Twillio received [%s] from [%s]", question, client_number)

        answer = self.ask_question(client_number, question)

        response = self.create_response(client_number, answer)

        YLogger.debug(self, "Twillio sending [%s] to [%s]", answer, client_number)

        return response


if __name__ == "__main__":

    print("Initiating Twilio Client...")

    TWILIO_CLIENT = TwilioBotClient()

    APP = Flask(__name__)

    print("Exposing endpoint: "+TWILIO_CLIENT.configuration.client_configuration.api)
    @APP.route(TWILIO_CLIENT.configuration.client_configuration.api, methods=['POST'])
    def receive_message():
        try:
            return TWILIO_CLIENT.receive_message(request)
        except Exception as e:
            YLogger.exception(None, "Twilio Error", e)

    TWILIO_CLIENT.run(APP)
