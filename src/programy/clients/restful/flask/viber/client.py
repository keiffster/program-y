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

# https://developers.viber.com/docs/api/python-bot-api/

from programy.utils.logging.ylogger import YLogger

from flask import Flask, request, Response

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from viberbot.api.messages.text_message import TextMessage

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.viber.config import ViberConfiguration


VIBER_CLIENT = None


class ViberBotClient(FlaskRestBotClient):

    _running = False

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, "viber", argument_parser)

        YLogger.debug(self, "Viber Client is running....")

        self._viber_bot = self.create_viber_bot(self._viber_token)

    def get_client_configuration(self):
        return ViberConfiguration()

    def get_license_keys(self):
        self._viber_token = self.license_keys.get_key("VIBER_TOKEN")

    def create_viber_api(self, configuration):
        return Api(configuration)

    def create_viber_bot(self, viber_token):

        if viber_token is None:
            YLogger.error(self, "'viber_token' missing")
            return None

        name = self.configuration.client_configuration.name
        if name is None:
            YLogger.error(self, "'name' missing from Viber configuration")
            return None

        avatar = self.configuration.client_configuration.avatar
        if avatar is None:
            YLogger.error(self, "'avatar' missing from Viber configuration")
            return None

        webhook = self.configuration.client_configuration.webhook
        if webhook is None:
            YLogger.error(self, "'webhook' missing from Viber configuration")
            return None

        configuration = BotConfiguration(
            name=name,
            avatar=avatar,
            auth_token=viber_token
        )

        bot = self.create_viber_api(configuration)
        if bot is not None:
            YLogger.error(self, "'Failed to create Viber api")

        bot.set_webhook(webhook)
        return bot

    def handle_message_request(self, viber_request):
        message = viber_request.message
        userid = viber_request.sender.id

        response = self.ask_question(userid, message)

        self._viber_bot.send_messages(viber_request.sender.id, [
            TextMessage(text=response)
        ])

    def handle_subscribed_request(self, viber_request):
        self._viber_bot.send_messages(viber_request.user.id, [
            TextMessage(text="Thanks for subscribing!")
        ])

    def handle_unsubscribed_request(self, viber_request):
        pass

    def handle_conversation_started_request(self, viber_request):
        pass

    def handle_failed_request(self, viber_request):
        pass

    def handle_unknown_request(self, viber_request):
        YLogger.error(self, "client failed receiving message. failure: {0}".format(viber_request))

    def receive_message(self, request):

        if self.configuration.client_configuration.debug is True:
            self.dump_request(request)

        # every viber message is signed, you can verify the signature using this method
        if not self._viber_bot.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
            return Response(status=403)

        # this library supplies a simple way to receive a request object
        viber_request = self._viber_bot.parse_request(request.get_data())

        if isinstance(viber_request, ViberMessageRequest):
            self.handle_message_request(viber_request)

        elif isinstance(viber_request, ViberSubscribedRequest):
            self.handle_subscribed_request(viber_request)

        elif isinstance(viber_request, ViberUnsubscribedRequest):
            self.handle_unsubscribed_request(viber_request)

        elif isinstance(viber_request, ViberConversationStartedRequest):
            self.handle_conversation_started_request(viber_request)

        elif isinstance(viber_request, ViberFailedRequest):
            self.handle_failed_request(viber_request)

        else:
            self.handle_unknown_request(viber_request)

        return Response(status=200)


if __name__ == "__main__":

    print("Initiating Viber Client...")

    VIBER_CLIENT = ViberBotClient()

    APP = Flask(__name__)

    @APP.route(VIBER_CLIENT.configuration.client_configuration.api, methods=['POST'])
    def receive_message():
        try:
            return VIBER_CLIENT.receive_message(request)
        except Exception as e:
            YLogger.exception(None, "Viber error", e)

    VIBER_CLIENT.run(APP)
