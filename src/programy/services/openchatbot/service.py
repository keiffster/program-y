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

# <sraix service="OPENCHAT"> @botname question </sraix>

from programy.utils.logging.ylogger import YLogger
from urllib.parse import quote

from programy.services.rest import GenericRESTService
from programy.config.brain.service import BrainServiceConfiguration
from programy.clients.restful.apikeys import APIKeysHandler
from programy.clients.restful.auth import RestBasicAuthorizationHandler
from programy.services.openchatbot.parser import OpenChatBotResponseParser


class OpenChatRESTService(GenericRESTService):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        GenericRESTService.__init__(self, config, api)

    def _format_post_payload(self, client_context, question, lang=None, location=None):
        payload = {'query': question,
                   "userId": client_context.userid}

        if lang is not None:
            payload["lang"] = lang

        if location is not None:
            payload["location"] = location

        return payload

    def _format_get_url(self, url, client_context, question, lang=None, location=None, api_key=None):
        get_url = "%s?query=%s&userId=%s"%(url, quote(question), client_context.userid)

        if lang is not None:
            get_url = "%s&lang=%s"%(get_url, lang)

        if location is not None:
            get_url = "%s&location=%s"%(get_url, location)

        if api_key is not None:
            get_url = "%s&%s"%(get_url, APIKeysHandler.format_get_api_key_param(api_key))

        return get_url

    def _parse_response(self, client_context, text):
        parser = OpenChatBotResponseParser()
        parser.parse_response(text)

        if parser.status.code == 200:
            return parser.response.to_aiml()

        return client_context.bot.default_response

    def _parse_question(self, text):
        words = text.split()
        if len(words) < 2:
            raise Exception ("Query test too short [%s]"%text)

        botname = words[0]

        query = " ".join(words[1:])

        return botname, query

    def _get_openchatbot(self, client_context, botname):

        openchatbot = client_context.brain.openchatbots.openchatbot(botname)

        if openchatbot is not None:
            return openchatbot

        raise Exception ("No open chatbot available for [%s]"% botname)

    def ask_question(self, client_context, question: str):

        try:
            botname, query = self._parse_question(question)

            chatbot = self._get_openchatbot(client_context, botname)

            headers = {}

            if self.method == 'GET' and self.method in chatbot.methods:
                full_url = self._format_get_url(chatbot.url, client_context, query, api_key=chatbot.api_key)

                if chatbot.authorization == 'Basic':
                    RestBasicAuthorizationHandler.add_authorisation_header(client_context, headers)

                    response = self.api.get(full_url, headers=headers)

                else:
                    response = self.api.get(full_url)

            elif self.method == 'POST' and self.method in chatbot.methods:
                payload = self._format_post_payload(client_context, query)
                if chatbot.authorization == 'Basic' or chatbot.api_key is not None:

                    if chatbot.authorization == 'Basic':
                        RestBasicAuthorizationHandler.add_authorisation_header(client_context, headers)

                    if chatbot.api_key is not None:
                        APIKeysHandler.add_post_api_key_header(headers, chatbot.api_key)

                    response = self.api.post(chatbot.url, data=payload, headers=headers)
                else:
                    response = self.api.post(chatbot.url, data=payload)

            else:
                raise Exception("Unsupported REST method [%s]"%self.method)

            if response.status_code != 200:
                YLogger.error(client_context, "[%s] return status code [%d]", self.host, response.status_code)

            else:
                return self._parse_response(client_context, response.text)

        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)

        return ""


class OpenChatMetaBotRESTService(OpenChatRESTService):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        OpenChatRESTService.__init__(self, config, api)

    def _parse_response(self, client_context, text):
        print(text)
        return text
