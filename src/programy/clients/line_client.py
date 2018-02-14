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

# https://github.com/line/line-bot-sdk-python

import logging

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from programy.clients.client import BotClient
from programy.config.sections.client.line_client import LineConfiguration


LINE_CLIENT = None


class LineBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "line", argument_parser)

        self.get_tokens()

        self.create_line_bot()

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Line Client is running....")

    def set_environment(self):
        self.bot.brain.properties.add_property("env", 'line')

    def get_client_configuration(self):
        return LineConfiguration()

    def get_tokens(self):
        self._channel_secret = self.bot.license_keys.get_key("LINE_CHANNEL_SECRET")
        self._channel_access_token = self.bot.license_keys.get_key("LINE_ACCESS_TOKEN")

    def ask_question(self, clientid, question):
        response = ""
        try:
            response = self.bot.ask_question(clientid, question)
        except Exception as e:
            print(e)
        return response

    def create_line_bot(self):
        self._line_bot_api = LineBotApi(self._channel_access_token)
        self._parser = WebhookParser(self._channel_secret)

    def handle_text_message(self, event):
        question = event.message.text
        clientid = event.source.user_id

        answer = self.ask_question(clientid, question)

        self._line_bot_api.reply_message(event.reply_token, TextSendMessage(text=answer))

    def handle_unknown_event(self, event):
        self._line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Sorry, I only handle text messages right now!"))

    def handle_unknown_message(self, event):
        self._line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Sorry, I only handle text messages right now!"))

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

    def handle_incoming(self, request):
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)

        # handle webhook body
        try:
            self.handle_message_request(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK'


APP = Flask(__name__)


@APP.route('/callback', methods=['POST'])
def incoming():
    return LINE_CLIENT.handle_incoming(request)


if __name__ == '__main__':


    LINE_CLIENT = LineBotClient()

    print("Line Client running on %s:%s" % (LINE_CLIENT.configuration.client_configuration.host,
                                             LINE_CLIENT.configuration.client_configuration.port))


    if LINE_CLIENT.configuration.client_configuration.debug is True:
        print("Line Client running in debug mode")

    if LINE_CLIENT.configuration.client_configuration.ssl_cert_file is not None and \
            LINE_CLIENT.configuration.client_configuration.ssl_key_file is not None:
        context = (LINE_CLIENT.configuration.client_configuration.ssl_cert_file,
                   LINE_CLIENT.configuration.client_configuration.ssl_key_file)

        print("Line Client running in https mode")
        APP.run(host=LINE_CLIENT.configuration.client_configuration.host,
                port=LINE_CLIENT.configuration.client_configuration.port,
                debug=LINE_CLIENT.configuration.client_configuration.debug,
                ssl_context=context)
    else:
        print("Line Client running in http mode, careful now !")
        APP.run(host=LINE_CLIENT.configuration.client_configuration.host,
                port=LINE_CLIENT.configuration.client_configuration.port,
                debug=LINE_CLIENT.configuration.client_configuration.debug)
