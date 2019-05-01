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
import os

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.alexa.config import AlexaConfiguration


class AlexaBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, 'alexa', argument_parser)

        YLogger.debug(self, "Alexa Client is running....")

        self._load_intent_mappings()

        print("Alexa Client loaded")

    def _load_intent_mappings(self):
        try:
            if self.configuration.client_configuration.intent_map_file is None:
                filename = os.path.dirname(__file__) + os.sep + "intents.maps"
            else:
                filename = self.configuration.client_configuration.intent_map_file

            with open(filename, 'r') as myfile:
                data = myfile.read()

            self._intent_mappings = json.loads(data)

        except Exception as e:
            print(e)
            self._intent_mappings = {}

    def get_client_configuration(self):
        return AlexaConfiguration()

    def _ask_question(self, client_context, question):
        reply = ""
        try:
            self._questions += 1
            reply = client_context.bot.ask_question(client_context, question, responselogger=self)

        except Exception as e:
            YLogger.exception(client_context, "Error getting reply from bot", e)

        return reply

    def _to_json(self, data):
        return jsonify(data)

    def _create_response(self, response, type="PlainText", playBehavior="REPLACE_ENQUEUED", shouldEndSession=False):
        reply = {}
        reply["version"] = "1.0"
        reply["response"] = {}
        if reply is not None:
            ssml_reply = "<speak>%s</speak>" % response
            reply["response"]["outputSpeech"] = {}
            reply["response"]["outputSpeech"]["type"] = type
            reply["response"]["outputSpeech"]["text"] = response
            reply["response"]["outputSpeech"]["ssml"] = ssml_reply
            reply["response"]["outputSpeech"]["playBehavior"] = playBehavior
        reply["response"]["shouldEndSession"] = shouldEndSession
        return self._to_json(reply)

    def _extract_question(self, intent):
        if 'slots' in intent:
            slots = intent['slots']

            if 'text' in slots:
                text_slot = slots['text']

                if 'value' in text_slot:
                   return text_slot['value']

        return ""

    def _add_intent(self, intent_name, value):
        if intent_name in self._intent_mappings:
            return "%s %s" % (self._intent_mappings[intent_name], value)

        return value

    def _should_leave(self, intent_name):
        if intent_name in self.configuration.client_configuration.leave_intents:
            return True
        return False

    def get_reply_from_bot(self, client_context, text, srai):
        if srai is not None:
            reply = self._ask_question(client_context, srai)
            if reply is None or reply == "":
                reply = text
        else:
            reply = text

        return reply

    def _handle_launch_request(self, client_context):
        print("Handling launch...")
        if self.configuration.client_configuration.launch_srai is not None:
            reply = self._ask_question(client_context, self.configuration.client_configuration.launch_srai)

        else:
            reply = self.configuration.client_configuration.launch_text

        return self._create_response(reply)

    def _handle_intent_request(self, client_context, request):

        if 'intent' not in request:
            raise Exception ("Invalid request, intent missing!")

        intent = request['intent']

        if 'name' not in intent:
            raise Exception ("Invalid intent, name missing!")

        intent_name = intent['name']

        print("Handling [%s] intent..."%intent_name)

        if intent_name == 'AMAZON.CancelIntent':
            return self._handle_cancel_request(client_context, self._should_leave(intent_name))

        elif intent_name == 'AMAZON.StopIntent':
            return self._handle_stop_request(client_context, self._should_leave(intent_name))

        elif intent_name == 'AMAZON.HelpIntent':
            return self._handle_help_request(client_context)

        else:
            value = self._extract_question(intent)

            question = self._add_intent(intent_name, value)

            return self._handle_reply_request(client_context, question)

    def _handle_leave_request(self):
        return self._create_response("See you later, aligator", shouldEndSession=True)

    def _handle_reply_request(self, client_context, question):
        reply = self._ask_question(client_context, question)
        return self._create_response(reply)

    def _handle_cancel_request(self, client_context, shouldEndSession=False):
        reply = self.get_reply_from_bot(client_context, self.configuration.client_configuration.cancel_text,
                                         self.configuration.client_configuration.cancel_srai)
        return self._create_response(reply, shouldEndSession=shouldEndSession)

    def _handle_stop_request(self, client_context, shouldEndSession=False):
        reply = self.get_reply_from_bot(client_context, self.configuration.client_configuration.stop_text,
                                         self.configuration.client_configuration.stop_srai)
        return self._create_response(reply, shouldEndSession=shouldEndSession)

    def _handle_help_request(self, client_context):
        reply = self.get_reply_from_bot(client_context, self.configuration.client_configuration.help_text,
                                         self.configuration.client_configuration.help_srai)
        return self._create_response(reply)

    def _handle_error(self, client_context):
        reply = self.get_reply_from_bot(client_context, self.configuration.client_configuration.error_text,
                                         self.configuration.client_configuration.error_srai)
        return self._create_response(reply)

    def _get_userid(self, request):
        if 'session' not in request:
            raise Exception ("Invalid request, session missing")

        if "user" not in request['session']:
            raise Exception ("Invalid session, user missing")

        if "userId" not in request['session']['user']:
            raise Exception ("Invalid user, userId missing")

        return request['session']['user']['userId']

    def receive_message(self, http_request):

        skill_json = http_request.json

        recipient_id = self._get_userid(skill_json)

        if 'request' not in skill_json:
            raise Exception ("Invalid HTTP request, request missing!")

        skill_request = skill_json['request']

        if 'type' not in skill_request:
            raise Exception ("Invalid skill request, type missing!")

        request_type = skill_request['type']

        client_context = self.create_client_context(recipient_id)

        try:
            if request_type == 'LaunchRequest':
                return self._handle_launch_request(client_context)

            elif request_type == 'IntentRequest':
                return self._handle_intent_request(client_context, skill_request)

            elif request_type == 'SessionEndedRequest':
                return self._handle_stop_request(client_context, shouldEndSession=True)

            else:
                raise Exception("Unknown/Unhandled request")

        except Exception as e:
            YLogger.exception(client_context, "Unknown/Unhandled request [%s]", e, request_type)
            return self._handle_error(client_context)


if __name__ == "__main__":

    print("Initiating Alexa Client...")

    ALEXA_CLIENT = AlexaBotClient()

    APP = Flask(__name__)

    @APP.route(ALEXA_CLIENT.configuration.client_configuration.api, methods=['GET', 'POST'])
    def receive_message():
        try:
            return ALEXA_CLIENT.receive_message(request)
        except Exception as e:
            print(e)
            YLogger.exception(None, "Alexa Error", e)

    ALEXA_CLIENT.run(APP)
