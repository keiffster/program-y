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

import logging
import datetime

from programy.dialog.dialog import Conversation, Question, Sentence
from programy.dialog.storage.factory import ConversationStorageFactory
from programy.config.sections.bot.bot import BotConfiguration
from programy.utils.license.keys import LicenseKeys
from programy.utils.classes.loader import ClassLoader
from programy.utils.files.filewriter import ConversationFileWriter

class Bot(object):

    def __init__(self, brain, config: BotConfiguration):
        self._brain = brain
        self._configuration = config

        self._conversations = {}
        self._question_depth = 0
        self._question_start_time = None
        self._spell_checker = None
        self._conversation_storage = None
        self._license_keys = None

        self.conversation_logger = None
        if self.brain.configuration.files.aiml_files.conversation is not None:
            self.conversation_logger = ConversationFileWriter(self.brain.configuration.files.aiml_files.conversation)

        self.load_license_keys()

        self.initiate_spellchecker()

        self.initiate_conversation_storage()

    @property
    def configuration(self):
        return self._configuration

    def load_license_keys(self):
        # TODO Move this to License keys base class
        self._license_keys = LicenseKeys()
        if self._configuration is not None:
            self._load_license_keys(self._configuration)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("No configuration defined when loading license keys")

    def _load_license_keys(self, bot_configuration):
        if bot_configuration.license_keys is not None:
            self._license_keys.load_license_key_file(bot_configuration.license_keys)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("No configuration setting for license_keys")

    def initiate_spellchecker(self):
        # TODO Move this to Spelling bass class
        if self._configuration is not None:
            if self._configuration.spelling.classname is not None:
                try:
                    if logging.getLogger().isEnabledFor(logging.INFO):
                        logging.info("Loading spelling checker from class [%s]", self._configuration.spelling.classname)
                    spell_class = ClassLoader.instantiate_class(self._configuration.spelling.classname)
                    self._spell_checker = spell_class(self._configuration.spelling)
                except Exception as excep:
                    logging.exception(excep)
            else:
                if logging.getLogger().isEnabledFor(logging.WARNING):
                    logging.warning("No configuration setting for spelling checker!")

    @property
    def spell_checker(self):
        return self._spell_checker

    @property
    def brain(self):
        return self._brain

    @property
    def conversations(self):
        return self._conversations

    @property
    def license_keys(self):
        return self._license_keys

    @property
    def prompt(self):
        if self._configuration is not None:
            return self._configuration.prompt
        return BotConfiguration.DEFAULT_PROMPT

    @property
    def default_response(self):
        if self._configuration is not None:
            return self._configuration.default_response
        return BotConfiguration.DEFAULT_RESPONSE

    @property
    def default_response_srai(self):
        if self._configuration is not None:
            return self._configuration.default_response_srai
        return None

    @property
    def exit_response(self):
        if self._configuration is not None:
            return self._configuration.exit_response
        return BotConfiguration.DEFAULT_EXIT_RESPONSE

    @property
    def exit_response_srai(self):
        if self._configuration is not None:
            return self._configuration.exit_response_srai
        return BotConfiguration.DEFAULT_EXIT_RESPONSE_SRAI

    @property
    def initial_question(self):
        if self._configuration is not None:
            return self._configuration.initial_question
        return BotConfiguration.DEFAULT_INITIAL_QUESTION

    @property
    def initial_question_srai(self):
        if self._configuration is not None:
            return self._configuration.initial_question_srai
        return BotConfiguration.DEFAULT_INITIAL_QUESTION_SRAI

    @property
    def override_properties(self):
        if self._configuration is not None:
            return self._configuration.override_properties
        return False

    @property
    def get_version_string(self):
        if self._configuration is not None:
            if self.brain.properties.has_property("version"):
                # The old version of returning the version string, did not distinquish
                # between App and Grammar version
                return "%s, v%s, initiated %s" % (
                    self.brain.properties.property("name"),
                    self.brain.properties.property("version"),
                    self.brain.properties.property("birthdate"))
            else:
                # This version now does
                return "%s, App: v%s Grammar v%s, initiated %s" % (
                    self.brain.properties.property("name"),
                    self.brain.properties.property("app_version"),
                    self.brain.properties.property("grammar_version"),
                    self.brain.properties.property("birthdate"))
        return ""

    def has_conversation(self, clientid):
        return bool(clientid in self._conversations)

    def conversation(self, clientid: str):
        return self.get_conversation(clientid)

    def get_conversation(self, clientid: str):
        # TODO move this to Conversations base class
        if clientid in self._conversations:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Retrieving conversation for client %s", clientid)
            return self._conversations[clientid]
        else:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Creating new conversation for client %s", clientid)

            conversation = Conversation(clientid, self)

            if self.brain.properties is not None:
                conversation.load_initial_variables(self.brain.variables)

            self._conversations[clientid] = conversation

            self.load_conversation(clientid)

            return conversation

    def initiate_conversation_storage(self):
        if self._configuration is not None:
            if self._configuration.conversations is not None:
                self._conversation_storage = ConversationStorageFactory.get_storage(self._configuration)
                if self._conversation_storage is not None:
                    if self._configuration.conversations.empty_on_start is True:
                        self._conversation_storage.empty ()

    def load_conversation(self, clientid):
        if self._conversation_storage is not None:
            if clientid in self._conversations:
                conversation = self._conversations[clientid]
                self._conversation_storage.load_conversation(conversation, clientid,
                                                             self.configuration.conversations.restore_last_topic)

    def save_conversation(self, clientid):
        if self._conversation_storage is not None:
            if clientid in self._conversations:
                conversation = self._conversations[clientid]
                self._conversation_storage.save_conversation(conversation, clientid)
            else:
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("Unknown conversation id type [%s] unable tonot persist!" % clientid)

    def check_max_recursion(self):
        if self._configuration.max_question_recursion != -1:
            if self._question_depth > self._configuration.max_question_recursion:
                raise Exception("Maximum recursion limit [%d] exceeded" % self._configuration.max_question_recursion)

    def total_search_time(self):
        delta = datetime.datetime.now() - self._question_start_time
        return abs(delta.total_seconds())

    def check_max_timeout(self):
        if self._configuration.max_question_timeout != -1:
            if self.total_search_time() >= self._configuration.max_question_timeout:
                raise Exception("Maximum search time limit [%d] exceeded" % self._configuration.max_question_timeout)

    def check_spelling_before(self, each_sentence):
        # TODO Move this to spelliing base class
        if self._configuration.spelling.check_before is True:
            text = each_sentence.text()
            corrected = self.spell_checker.correct(text)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Spell Checker corrected [%s] to [%s]", text, corrected)
            each_sentence.replace_words(corrected)

    def check_spelling_and_retry(self, clientid, each_sentence):
        # TODO Move this to spelling base class
        if self._configuration.spelling.check_and_retry is True:
            text = each_sentence.text()
            corrected = self.spell_checker.correct(text)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Spell Checker corrected [%s] to [%s]", text, corrected)
            each_sentence.replace_words(corrected)
            response = self.brain.ask_question(self, clientid, each_sentence)
            return response
        return None

    def ask_question(self, clientid: str, text: str, srai=False, responselogger=None):
        # TODO Method too big, convert to smaller methods

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("##########################################################################################")
            logging.debug("Question (%s): %s", clientid, text)

        if srai is False:
            pre_processed = self.brain.pre_process_question(self, clientid, text)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Pre Processed (%s): %s", clientid, pre_processed)
        else:
            pre_processed = text

        if pre_processed is None or pre_processed == "":
            pre_processed = self._configuration.empty_string

        if srai is False:
            question = Question.create_from_text(self.brain.tokenizer,pre_processed)
        else:
            question = Question.create_from_text(self.brain._tokenizer, pre_processed, split=False)

        conversation = self.get_conversation(clientid)
        conversation.record_dialog(question)

        if self._question_depth == 0:
            self._question_start_time = datetime.datetime.now()
        self._question_depth += 1

        answers = []
        sentence_no = 0
        for each_sentence in question.sentences:

            question.set_current_sentence_no(sentence_no)

            self.check_max_recursion()
            self.check_max_timeout()

            if srai is False:
                self.check_spelling_before(each_sentence)

            response = self.brain.ask_question(self, clientid, each_sentence, srai=srai)

            if response is None and srai is False:
                response = self.check_spelling_and_retry(clientid, each_sentence)

            if response is not None:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("Raw Response (%s): %s", clientid, response)
                each_sentence.response = response

                if srai is False:
                    answer = self.brain.post_process_response(self, clientid, response).strip()
                    if not answer:
                        answer = self.get_default_response(clientid)
                else:
                    answer = response

                answers.append(answer)
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("Processed Response (%s): %s", clientid, answer)

                if responselogger is not None:
                    responselogger.log_response(each_sentence.text, answer)

            else:
                default_response = self.get_default_response(clientid)
                each_sentence.response = default_response
                answers.append(default_response)

                if responselogger is not None:
                    responselogger.log_unknown_response(each_sentence)

            sentence_no += 1

        self._question_depth = 0

        if srai is True:
            conversation.pop_dialog()

        response = ". ".join([sentence for sentence in answers if sentence is not None])

        if self.conversation_logger is not None:
            self.conversation_logger.log_question_and_answer(clientid, text, response)

        return response

    def get_default_response(self, clientid):
        if self.default_response_srai is not None:
            sentence = Sentence(self.brain.tokenizer, self.default_response_srai)
            default_response = self.brain.ask_question(self, clientid, sentence, srai=False)
            if default_response is None or not default_response:
                default_response = self.default_response
            return default_response
        else:
            return self.default_response

    def get_initial_question(self, clientid):
        if self.initial_question_srai is not None:
            sentence = Sentence(self.brain.tokenizer, self.initial_question_srai)
            initial_question = self.brain.ask_question(self, clientid, sentence, srai=False)
            if initial_question is None or not initial_question:
                initial_question = self.initial_question
            return initial_question
        else:
            return self.initial_question

    def get_exit_response(self, clientid):
        if self.exit_response_srai is not None:
            sentence = Sentence(self.brain.tokenizer, self.exit_response_srai)
            exit_response = self.brain.ask_question(self, clientid, sentence, srai=False)
            if exit_response is None or not exit_response:
                exit_response = self.exit_response
            return exit_response
        else:
            return self.exit_response

