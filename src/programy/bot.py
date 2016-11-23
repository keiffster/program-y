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
from programy.config import BotConfiguration

class Bot(object):

    def __init__(self, brain, config: BotConfiguration):
        self._brain = brain
        self._configuration = config
        self._conversations = {}

    @property
    def brain(self):
        return self._brain

    @property
    def conversations(self):
        return self._conversations

    @property
    def prompt (self):
        if self._configuration is not None:
            return self._configuration.prompt
        else:
            return ">>> "

    @property
    def default_response(self):
        if self._configuration is not None:
            return self._configuration.default_response
        else:
            #return "Sorry, I don't have an answer for that right now"
            return ""

    @property
    def exit_response(self):
        if self._configuration is not None:
            return self._configuration.exit_response
        else:
            return "Bye!"

    @property
    def initial_question(self):
        if self._configuration is not None:
            return self._configuration.initial_question
        else:
            return "Hello"

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
        if clientid in self._conversations:
            return True
        else:
            return False

    def conversation(self, clientid: str):
        return self.get_conversation(clientid)

    def get_conversation(self, clientid: str):
        if clientid in self._conversations:
            logging.info ("Retrieving conversation for client %s"%(clientid))
            return self._conversations[clientid]
        else:
            logging.info ("Creating new conversation for client %s"%(clientid))
            conversation = Conversation(clientid, self)
            self._conversations[clientid] = conversation
            return conversation

    def ask_question(self, clientid: str, text: str):

        logging.debug("Question (%s): %s"%(clientid, text))

        pre_processed = self.brain.pre_process_question(text)
        logging.debug("Pre Processed (%s): %s"%(clientid, pre_processed))

        conversation = self.get_conversation(clientid)

        question = Question.create_from_text(pre_processed)
        conversation.record_dialog(question)

        for each_sentence in question._sentences:
            response = self.brain.ask_question(self, clientid, each_sentence)
            if response is not None:
                logging.debug("Raw Response (%s): %s"%(clientid, response))
                each_sentence.response = self.brain.post_process_response(response).strip()
                logging.debug("Processed Response (%s): %s"%(clientid, each_sentence.response))
            else:
                each_sentence.response = self.default_response

        return question.combine_answers()

