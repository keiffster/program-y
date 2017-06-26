"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.dialog import Conversation, Question
from programy.config.bot import BotConfiguration
from programy.utils.license.keys import LicenseKeys

class Bot(object):

    def __init__(self, brain, config: BotConfiguration):
        self._brain = brain
        self._configuration = config
        self._conversations = {}
        self._license_keys = LicenseKeys()
        self._load_license_keys(self._configuration)
        self._question_depth = 0

    @property
    def brain(self):
        return self._brain

    @property
    def conversations(self):
        return self._conversations

    @property
    def license_keys(self):
        return self._license_keys

    def _load_license_keys(self, bot_configuration):
        if bot_configuration.license_keys is not None:
            self._license_keys.load_license_key_file(bot_configuration.license_keys)
        else:
            logging.warning("No configuration setting for license_keys")

    @property
    def prompt(self):
        if self._configuration is not None:
            return self._configuration.prompt
        else:
            return BotConfiguration.DEFAULT_PROMPT

    @property
    def default_response(self):
        if self._configuration is not None:
            return self._configuration.default_response
        else:
            return BotConfiguration.DEFAULT_RESPONSE

    @property
    def exit_response(self):
        if self._configuration is not None:
            return self._configuration.exit_response
        else:
            return BotConfiguration.DEFAULT_EXIT_RESPONSE

    @property
    def initial_question(self):
        if self._configuration is not None:
            return self._configuration.initial_question
        else:
            return BotConfiguration.DEFAULT_INITIAL_QUESTION

    @property
    def override_predicates(self):
        return self._configuration.override_predicates

    @property
    def get_version_string(self):
        if self._configuration is not None:
            return "%s version %s, initiated %s" %(
                self.brain.properties.property("name"),
                self.brain.properties.property("version"),
                self.brain.properties.property("birthdate"))
        else:
            return ""

    def has_conversation(self, clientid):
        return bool(clientid in self._conversations)

    def conversation(self, clientid: str):
        return self.get_conversation(clientid)

    def get_conversation(self, clientid: str):
        if clientid in self._conversations:
            logging.info("Retrieving conversation for client %s", clientid)
            return self._conversations[clientid]
        else:
            logging.info("Creating new conversation for client %s", clientid)
            conversation = Conversation(clientid, self)
            self._conversations[clientid] = conversation
            return conversation

    def ask_question(self, clientid: str, text: str, srai=False):

        logging.debug("Question (%s): %s", clientid, text)

        if srai is False:
            pre_processed = self.brain.pre_process_question(self, clientid, text)
            logging.debug("Pre Processed (%s): %s", clientid, pre_processed)
        else:
            pre_processed = text

        if len(pre_processed) == 0:
            pre_processed = self._configuration.empty_string

        conversation = self.get_conversation(clientid)

        if srai is False:
            question = Question.create_from_text(pre_processed)
        else:
            question = Question.create_from_text(pre_processed, split=False)

        conversation.record_dialog(question)

        answers = []
        for each_sentence in question.sentences:

            self._question_depth += 1
            if self._question_depth > self._configuration.max_recursion:
                raise Exception ("Maximum recursion limit [%d] exceeded"%(self._configuration.max_recursion))

            response = self.brain.ask_question(self, clientid, each_sentence)
            if response is not None:
                logging.debug("Raw Response (%s): %s", clientid, response)
                each_sentence.response = response

                if srai is False:
                    answer = self.brain.post_process_response(self, clientid, response).strip()
                    if len(answer) == 0:
                        answer = self.default_response
                else:
                    answer = response

                answers.append(answer)
                logging.debug("Processed Response (%s): %s", clientid, answer)
            else:
                each_sentence.response = self.default_response
                answers.append(self.default_response)

            self._question_depth = 0

        if srai is True:
            conversation.pop_dialog()

        return ". ".join([sentence for sentence in answers if sentence is not None])
