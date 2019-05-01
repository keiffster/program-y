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
from programy.utils.logging.ylogger import YLogger

import http.server
import json
import asyncio
from botbuilder.schema import (Activity, ActivityTypes)
from botframework.connector import ConnectorClient
from botframework.connector.auth import (MicrosoftAppCredentials, JwtTokenValidation, SimpleCredentialProvider)

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.asyncio.microsoft.config import MicrosoftConfiguration


class MicrosoftBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, 'microsoft', argument_parser)

        YLogger.debug(self, "Microsoft Client is running....")

        print("Microsoft Client loaded")

    def get_client_configuration(self):
        return MicrosoftConfiguration()

    def get_microsoft_app_id(self):
        return self.license_keys.get_key("MICROSOFT_APP_ID")

    def get_microsoft_app_password(self):
        return self.license_keys.get_key("MICROSOFT_APP_PASSWORD")

    def get_new_user_message(self):
        if self.configuration.client_configuration.new_user_srai is not None:
            pass

        return self.configuration.client_configuration.new_user_text

    def ask_question(self, question):
        reply = ""
        try:
            client_context = self.create_client_context("microsoft")
            self._questions += 1
            reply = client_context.bot.ask_question(client_context, question, responselogger=self)

        except Exception as e:
            YLogger.exception(client_context, "Error getting reply from bot", e)

        return reply


MICROSOFT_CLIENT = MicrosoftBotClient ()


class BotRequestHandler(http.server.BaseHTTPRequestHandler):

    @staticmethod
    def __create_reply_activity(request_activity, text):
        return Activity(
            type=ActivityTypes.message,
            channel_id=request_activity.channel_id,
            conversation=request_activity.conversation,
            recipient=request_activity.from_property,
            from_property=request_activity.recipient,
            text=text,
            service_url=request_activity.service_url)

    def __handle_conversation_update_activity(self, activity):
        self.send_response(202)
        self.end_headers()
        if len(activity.members_added):
            if activity.members_added[0].id != activity.recipient.id:
                credentials = MicrosoftAppCredentials(MICROSOFT_CLIENT.get_microsoft_app_id(),
                                                      MICROSOFT_CLIENT.get_microsoft_app_password())

                response = MICROSOFT_CLIENT.get_new_user_message()
                reply = BotRequestHandler.__create_reply_activity(activity, response)

                connector = ConnectorClient(credentials, base_url=reply.service_url)
                connector.conversations.send_to_conversation(reply.conversation.id, reply)

    def __handle_message_activity(self, activity):
        self.send_response(200)
        self.end_headers()
        credentials = MicrosoftAppCredentials(MICROSOFT_CLIENT.get_microsoft_app_id(),
                                              MICROSOFT_CLIENT.get_microsoft_app_password())
        connector = ConnectorClient(credentials, base_url=activity.service_url)

        response = MICROSOFT_CLIENT.ask_question(activity.text)
        reply = BotRequestHandler.__create_reply_activity(activity, response)

        connector.conversations.send_to_conversation(reply.conversation.id, reply)

    def __handle_authentication(self, activity):
        credential_provider = SimpleCredentialProvider(MICROSOFT_CLIENT.get_microsoft_app_id(),
                                                       MICROSOFT_CLIENT.get_microsoft_app_password())
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(JwtTokenValidation.authenticate_request(activity,
                                                                            self.headers.get("Authorization"),
                                                                            credential_provider))
            return True
        except Exception as ex:
            self.send_response(401, ex)
            self.end_headers()
            return False
        finally:
            loop.close()

    def __unhandled_activity(self):
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(str(body, 'utf-8'))
        activity = Activity.deserialize(data)

        if not self.__handle_authentication(activity):
            return

        if activity.type == ActivityTypes.conversation_update.value:
            self.__handle_conversation_update_activity(activity)
        elif activity.type == ActivityTypes.message.value:
            self.__handle_message_activity(activity)
        else:
            self.__unhandled_activity()


if __name__ == '__main__':

    print("Initiating Microsoft Client...")

    SERVER = None
    try:
        host = MICROSOFT_CLIENT.configuration.client_configuration.host
        port = MICROSOFT_CLIENT.configuration.client_configuration.port

        SERVER = http.server.HTTPServer((host, port), BotRequestHandler)
        print('Started http server')
        SERVER.serve_forever()

    except KeyboardInterrupt:
        print('Ctrl received, shutting down server')
        if SERVER is not None:
            SERVER.socket.close()

