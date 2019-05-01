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

# https://kik.readthedocs.io/en/latest/user.html#installation

from programy.utils.logging.ylogger import YLogger

from flask import Flask, request, abort, Response

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.kik.config import KikConfiguration


class KikBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, "kik", argument_parser)

        self.create_kik_bot()

        YLogger.debug(self, "Kik Client is running....")

    def get_client_configuration(self):
        return KikConfiguration()

    def get_license_keys(self):
        self._bot_api_key = self.license_keys.get_key("KIK_BOT_API_KEY")

    def create_kik_bot(self):
        self._kik_bot = KikApi(self.configuration.client_configuration.bot_name, self._bot_api_key)
        self._kik_bot.set_configuration(Configuration(webhook=self.configuration.client_configuration.webhook))

    def handle_text_message(self, message):
        question = message.body
        userid = message.from_user

        answer = self.ask_question(userid, question)

        self._kik_bot.send_messages([
            TextMessage(
                to=message.from_user,
                chat_id=message.chat_id,
                body=answer
            )
        ])

    def get_unknown_response(self, userid):
        if self.configuration.client_configuration.unknown_command_srai is None:
            unknown_response = self.configuration.client_configuration.unknown_command
        else:
            unknown_response = self.ask_question(userid, self.configuration.client_configuration.unknown_command_srai)
            if unknown_response is None or unknown_response == "":
                unknown_response = self.configuration.client_configuration.unknown_command
        return unknown_response

    def handle_unknown_message(self, message):
        userid = message.from_user

        unknown_response = self.get_unknown_response(userid)

        self._kik_bot.send_messages([
            TextMessage(
                to=message.from_user,
                chat_id=message.chat_id,
                body=unknown_response
            )
        ])

    def handle_message_request(self, request):

        messages = messages_from_json(request.json['messages'])

        for message in messages:
            if isinstance(message, TextMessage):
                self.handle_text_message(message)
            else:
                self.handle_unknown_message(message)

    def receive_message(self, request):

        if self.configuration.client_configuration.debug is True:
            self.dump_request(request)

        if not self._kik_bot.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
            return Response(status=403)

        self.handle_message_request(request)
        return Response(status=200)


if __name__ == "__main__":

    print("Initiating Kik Client...")

    KIK_CLIENT = KikBotClient()

    APP = Flask(__name__)

    @APP.route(KIK_CLIENT.configuration.client_configuration.api, methods=['POST'])
    def receive_message():
        try:
            return KIK_CLIENT.receive_message(request)
        except Exception as e:
            YLogger.exception(None, "KIK Error", e)

    KIK_CLIENT.run(APP)
