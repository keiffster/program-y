"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import re
from abc import ABC
from abc import abstractmethod
from programy.dialog.sentence import Sentence
from programy.utils.logging.ylogger import YLogger


class ServiceException(Exception):

    def __init__(self, msg: str):
        Exception.__init__(self, msg)


class ServiceQuery(ABC):

    def __init__(self, service):
        self._service = service

    def parse_matched(self, matched):
        pass

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def aiml_response(self, response):
        YLogger.debug(self, response)
        return response

    @staticmethod
    def _get_matched_var(matched, index, name, optional=False):
        try:
            value = matched[index]

            if value is 'NONE':
                return None
            return value.strip()

        except:
            if optional is False:
                raise ValueError("query variable [%s] missing" % name)

        return None


class Service:

    DEFAULT_RESPONSE = "Service failed to return valid response"

    def __init__(self, configuration):
        self._configuration = configuration

    @property
    def configuration(self):
        return self._configuration

    @property
    def category(self) -> str:
        return self.configuration.category

    @property
    def name(self) -> str:
        return self.configuration.name

    def patterns(self) -> list:
        return []

    def initialise(self, client):
        pass

    def _match(self, question: str):
        """For each pattern for the grammar, try to find a match"""
        for pattern in self.patterns():
            matched = re.match(pattern[0], question, re.IGNORECASE)
            if matched is not None:
                query = pattern[1].create(self)
                if query is not None:
                    query.parse_matched(matched.groups())
                    YLogger.debug(self, "Service matched question [{0}] to pattern [{0}]".format(question, pattern[0]))
                    return query

        return None

    def execute_query(self, question, aiml=False):
        query = self._match(question)
        if query is not None:
            response = query.execute()
            if response is not None:
                if response['response']['status'] == 'success':
                    if aiml is True:
                        if self.configuration.success_prefix is not None:
                            result = "{0} {1}".format(self.configuration.success_prefix, query.aiml_response(response))
                        else:
                            result = query.aiml_response(response)
                    else:
                        result = response

                    YLogger.debug(self, result)
                    return result

                YLogger.error(self, "Service failed to execute query [%s] - [%s]", question, response)

        YLogger.debug(self, "Service failed to execute query [%s], empty response!", question)
        return None

    def _get_bot_response(self, client_context, sentence):
        return client_context.bot.ask_question(client_context, sentence)        # pragma: no cover

    def _get_default_response(self, client_context):
        response = None

        # Do we have an srai that we can ask the bot to expand on
        if self.configuration.default_srai is not None:
            sentence = Sentence(client_context, self.configuration.default_srai)
            response = client_context.bot.ask_question(client_context, sentence)

        # If not, do we have a default respond in the config
        if response is None:
            response = self.configuration.default_response

        # If not use the hard coded service default response
        if response is None:
            response = Service.DEFAULT_RESPONSE

        return response

    def ask_question(self, client_context, question):
        response = self.execute_query(question, aiml=True)

        # If we still don't have a response, get a default response
        if response is None:
            response = self._get_default_response(client_context)

        return response

    def get_default_aiml_file(self):
        return None

    def load_default_aiml(self, parser):

        if self.configuration.load_default_aiml is True:
            YLogger.debug(self, "Loading default aiml for service [%s]", self.name)

            filepath = None
            # First see if there is config option for default aiml
            if self.configuration.default_aiml is not None:
                filepath = self.configuration.default_aiml

            # If not then check if there is a internal name
            elif self.get_default_aiml_file() is not None:
                filepath = self.get_default_aiml_file()

            else:
                YLogger.info(self, "No default aiml for service [%s]", self.name)

            # If a file path exists, then load it into the parser
            if filepath is not None:
                return parser.parse_from_file(filepath, userid="*")

        return False
