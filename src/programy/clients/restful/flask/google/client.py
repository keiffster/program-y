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

from flask import Flask, request, jsonify
import json

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.google.config import GoogleConfiguration


class GoogleBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, 'google', argument_parser)

        YLogger.debug(self, "Google Client is running....")

        print("Google Client loaded")

    def _to_json(self, data):
        return self._to_json(data)

    def get_client_configuration(self):
        return GoogleConfiguration()

    def _ask_question(self, client_context, question):
        reply = ""
        try:
            self._questions += 1
            reply = client_context.bot.ask_question(client_context, question, responselogger=self)

        except Exception as e:
            YLogger.exception(client_context, "Error getting reply from bot", e)

        return reply

    def _get_reply_from_bot(self, client_context, text, srai):
        if srai is not None:
            reply = self._ask_question(client_context, srai)
            if reply is None or reply == "":
                reply = text
        else:
            reply = text

        return reply

    def _handle_launch_intent(self, client_context):
        response = self._get_reply_from_bot(client_context, self.configuration.client_configuration.launch_text,
                                            self.configuration.client_configuration.launch_srai)
        return self._to_json({"fulfillmentText": response})

    def _handle_quit_intent(self, client_context):
        response = self._get_reply_from_bot(client_context, self.configuration.client_configuration.quit_text,
                                            self.configuration.client_configuration.quit_srai)
        return self._to_json({"fulfillmentText": response})

    def _handle_help_intent(self, client_context):
        response = self._get_reply_from_bot(client_context, self.configuration.client_configuration.help_text,
                                            self.configuration.client_configuration.help_srai)
        return self._to_json({"fulfillmentText": response})

    def _handle_error(self, client_context):
        response = self._get_reply_from_bot(client_context, self.configuration.client_configuration.error_text,
                                            self.configuration.client_configuration.error_srai)
        return self._to_json({"fulfillmentText": response})

    def _handle_query_intent(self, client_context, query_result):

        if 'queryText' not in query_result:
            raise Exception("Invalid http queryResult, queryText missing!")
        query_text = query_result['queryText']

        response = self._ask_question(client_context, query_text)

        return self._to_json({"fulfillmentText": response})

    def _get_userid(self, skill_data):

        if 'session' in skill_data:
            return skill_data['session']

        return 'google'

    def receive_message(self, http_request):

        skill_data = json.loads(http_request.data)
        #print(json.dumps(skill_data, indent=4))

        if 'queryResult' not in skill_data:
            raise Exception("Invalid http request, queryResult missing!")
        queryResult = skill_data['queryResult']

        if 'intent' not in queryResult:
            raise Exception("Invalid queryResult, intent missing!")
        intent = queryResult['intent']

        if 'displayName' not in intent:
            raise Exception("Invalid intent, intent displayName!")

        userid = self._get_userid(skill_data)

        client_context = self.create_client_context(userid)

        intent_name = intent['displayName']

        try:
            if intent_name == 'Launch Intent':
                return self._handle_launch_intent(client_context)

            elif intent_name == 'Query Intent':
                return self._handle_query_intent(client_context, queryResult)

            elif intent_name == 'Quit Intent':
                return self._handle_quit_intent(client_context)

            elif intent_name == 'Help Intent':
                return self._handle_help_intent(client_context)

            else:
                raise Exception("Invalid intent name [%s]!", intent_name)

        except Exception as e:
            print(e)
            YLogger.exception(client_context, "Unknown/Unhandled intent [%s]", e, intent_name)
            return self._handle_error(client_context)


if __name__ == "__main__":

    print("Initiating Google Client...")

    GOOGLE_CLIENT = GoogleBotClient()

    APP = Flask(__name__)

    @APP.route("/api/google/v1.0/ask", methods=['GET', 'POST'])
    def receive_message():
        try:
            return GOOGLE_CLIENT.receive_message(request)
        except Exception as e:
            print(e)
            YLogger.exception(None, "Google Error", e)

    GOOGLE_CLIENT.run(APP)
