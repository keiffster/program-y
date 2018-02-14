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

# https://developers.viber.com/docs/api/python-bot-api/

import logging

from flask import Flask, request, Response

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from viberbot.api.messages.text_message import TextMessage

from programy.clients.client import BotClient
from programy.config.sections.client.viber_client import ViberConfiguration


VIBER_CLIENT = None


class ViberBotClient(BotClient):

    _running = False

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "viber", argument_parser)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Viber Client is running....")

        self._viber_token = self.get_token(self.bot.license_keys)

        self._viber_bot = self.create_viber_bot(self._viber_token)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", 'viber')

    def get_client_configuration(self):
        return ViberConfiguration()

    def get_token(self, license_keys):
        return license_keys.get_key("VIBER_TOKEN")

    def ask_question(self, bot, clientid, question):
        try:
            response = self.bot.ask_question(bot, clientid, question)
        except Exception as e:
            print(e)

    def create_viber_api(self, bot_configuration):
        return Api(bot_configuration)

    def create_viber_bot(self, viber_token):

        name = self.configuration.client_configuration.name
        avatar = self.configuration.client_configuration.avatar
        webhook = self.configuration.client_configuration.webhook

        bot_configuration = BotConfiguration(
            name=name,
            avatar=avatar,
            auth_token=viber_token
        )

        bot = self.create_viber_api(bot_configuration)

        bot.set_webhook(webhook)

        return bot

    def handle_message_request(self, viber_request):
        message = viber_request.message
        clientid = viber_request.sender.id

        self.ask_question(self.bot, clientid, message)

        self._viber_bot.send_messages(viber_request.sender.id, [
            message
        ])

    def handle_subscribed_request(self, viber_request):
        self._viber_bot.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])

    def handle_unsubscribed_request(self, viber_request):
        pass

    def handle_conversation_started_request(self, viber_request):
        pass

    def handle_failed_request(self, viber_request):
        pass

    def handle_unknown_request(self, viber_request):
        logging.error("client failed receiving message. failure: {0}".format(viber_request))

    def handle_incoming(self, request):
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

        elif isinstance(viber_request, ViberFailedRequest):
            self.handle_unknown_request(viber_request)

        return Response(status=200)


APP = Flask(__name__)


@APP.route('/incoming', methods=['POST'])
def incoming():
    return VIBER_CLIENT.handle_incoming(request)


if __name__ == '__main__':


    VIBER_CLIENT = ViberBotClient()

    print("Viber Client running on %s:%s" % (VIBER_CLIENT.configuration.client_configuration.host,
                                             VIBER_CLIENT.configuration.client_configuration.port))


    if VIBER_CLIENT.configuration.client_configuration.debug is True:
        print("Viber Client running in debug mode")

    if VIBER_CLIENT.configuration.client_configuration.ssl_cert_file is not None and \
            VIBER_CLIENT.configuration.client_configuration.ssl_key_file is not None:
        context = (VIBER_CLIENT.configuration.client_configuration.ssl_cert_file,
                   VIBER_CLIENT.configuration.client_configuration.ssl_key_file)

        print("Viber Client running in https mode")
        APP.run(host=VIBER_CLIENT.configuration.client_configuration.host,
                port=VIBER_CLIENT.configuration.client_configuration.port,
                debug=VIBER_CLIENT.configuration.client_configuration.debug,
                ssl_context=context)
    else:
        print("Viber Client running in http mode, careful now !")
        APP.run(host=VIBER_CLIENT.configuration.client_configuration.host,
                port=VIBER_CLIENT.configuration.client_configuration.port,
                debug=VIBER_CLIENT.configuration.client_configuration.debug)

