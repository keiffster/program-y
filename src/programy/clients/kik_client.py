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

# https://kik.readthedocs.io/en/latest/user.html#installation

import logging

from flask import Flask, request, abort, Response

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

from programy.clients.client import BotClient
from programy.config.sections.client.kik_client import KikConfiguration


KIK_CLIENT = None


class KikBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "kik", argument_parser)

        self.get_tokens()

        self.create_kik_bot()

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Kik Client is running....")

    def set_environment(self):
        self.bot.brain.properties.add_property("env", 'kik')

    def get_client_configuration(self):
        return KikConfiguration()

    def get_tokens(self):
        self._bot_api_key = self.bot.license_keys.get_key("KIK_BOT_API_KEY")

    def ask_question(self, clientid, question):
        response = ""
        try:
            response = self.bot.ask_question(clientid, question)
        except Exception as e:
            print(e)
        return response

    def create_kik_bot(self):
        self._kik_bot = KikApi(self.configuration.client_configuration.bot_name, self._bot_api_key)
        self._kik_bot.set_configuration(Configuration(webhook=self.configuration.client_configuration.webhook))

    def handle_text_message(self, message):
        question = message.body
        clientid = message.from_user

        answer = self.ask_question(clientid, question)

        self._kik_bot.send_messages([
            TextMessage(
                to=message.from_user,
                chat_id=message.chat_id,
                body=answer
            )
        ])

    def handle_unknown_message(self, message):
        pass

    def handle_message_request(self, request):

        messages = messages_from_json(request.json['messages'])

        for message in messages:
            if isinstance(message, TextMessage):
                self.handle_text_message(message)
            else:
                self.handle_unknown_message(message)

    def handle_incoming(self, request):
        if not self._kik_bot.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
            return Response(status=403)

        self.handle_message_request(request)
        return Response(status=200)


APP = Flask(__name__)


@APP.route('/incoming', methods=['POST'])
def incoming():
    return KIK_CLIENT.handle_incoming(request)


if __name__ == '__main__':

    KIK_CLIENT = KikBotClient()

    print("Kik Client running on %s:%s" % (KIK_CLIENT.configuration.client_configuration.host,
                                             KIK_CLIENT.configuration.client_configuration.port))


    if KIK_CLIENT.configuration.client_configuration.debug is True:
        print("Kik Client running in debug mode")

    if KIK_CLIENT.configuration.client_configuration.ssl_cert_file is not None and \
            KIK_CLIENT.configuration.client_configuration.ssl_key_file is not None:
        context = (KIK_CLIENT.configuration.client_configuration.ssl_cert_file,
                   KIK_CLIENT.configuration.client_configuration.ssl_key_file)

        print("Kik Client running in https mode")
        APP.run(host=KIK_CLIENT.configuration.client_configuration.host,
                port=KIK_CLIENT.configuration.client_configuration.port,
                debug=KIK_CLIENT.configuration.client_configuration.debug,
                ssl_context=context)
    else:
        print("Kik Client running in http mode, careful now !")
        APP.run(host=KIK_CLIENT.configuration.client_configuration.host,
                port=KIK_CLIENT.configuration.client_configuration.port,
                debug=KIK_CLIENT.configuration.client_configuration.debug)
