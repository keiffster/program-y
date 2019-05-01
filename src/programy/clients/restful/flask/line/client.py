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

# https://github.com/line/line-bot-sdk-python

from programy.utils.logging.ylogger import YLogger

from flask import Flask, request, abort, Response

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.line.config import LineConfiguration


class LineBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, "line", argument_parser)

        self.create_line_bot()

        YLogger.debug(self, "Line Client is running....")

    def get_client_configuration(self):
        return LineConfiguration()

    def get_license_keys(self):
        self._channel_secret = self.license_keys.get_key("LINE_CHANNEL_SECRET")
        self._channel_access_token = self.license_keys.get_key("LINE_ACCESS_TOKEN")

    def create_line_bot(self):
        self._line_bot_api = LineBotApi(self._channel_access_token)
        self._parser = WebhookParser(self._channel_secret)

    def handle_text_message(self, event):
        question = event.message.text
        userid = event.source.user_id

        answer = self.ask_question(userid, question)

        self._line_bot_api.reply_message(event.reply_token, TextSendMessage(text=answer))

    def get_unknown_response(self, userid):
        if self.configuration.client_configuration.unknown_command_srai is None:
            unknown_response = self.configuration.client_configuration.unknown_command
        else:
            unknown_response = self.ask_question(userid, self.configuration.client_configuration.unknown_command_srai)
            if unknown_response is None or unknown_response == "":
                unknown_response = self.configuration.client_configuration.unknown_command
        return unknown_response

    def handle_unknown_event(self, event):
        userid = ""
        unknown_response = self.get_unknown_response(userid)
        self._line_bot_api.reply_message(event.reply_token, TextSendMessage(text=unknown_response))

    def handle_unknown_message(self, event):
        userid = ""
        unknown_response = self.get_unknown_response(userid)
        self._line_bot_api.reply_message(event.reply_token, TextSendMessage(text=unknown_response))

    def handle_message_request(self, body, signature):

        events = self._parser.parse(body, signature)

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    self.handle_text_message(event)
                else:
                    self.handle_unknown_message(event)
            else:
                self.handle_unknown_event(event)

    def receive_message(self, request):

        if self.configuration.client_configuration.debug is True:
            self.dump_request(request)

        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)

        # handle webhook body
        try:
            self.handle_message_request(body, signature)
        except InvalidSignatureError as excep:
            YLogger.exception(self, "Line error", excep)
            abort(500)

        return Response(status=200)


if __name__ == "__main__":

    print("Initiating Line Client...")

    LINE_CLIENT = LineBotClient()

    APP = Flask(__name__)

    @APP.route(LINE_CLIENT.configuration.client_configuration.api, methods=['POST'])
    def receive_message():
        try:
            return LINE_CLIENT.receive_message(request)
        except Exception as e:
            YLogger.exception(None, "Line error", e)

    LINE_CLIENT.run(APP)
