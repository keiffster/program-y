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

from programy.config.base import BaseContainerConfigurationData
from programy.config.sections.bot.spelling import BotSpellingConfiguration
from programy.config.sections.bot.conversations import BotConversationsConfiguration


class BotConfiguration(BaseContainerConfigurationData):

    DEFAULT_ROOT = "."
    DEFAULT_PROMPT = ">>> "
    DEFAULT_RESPONSE = ""
    DEFAULT_RESPONSE_SRAI = ""
    DEFAULT_EMPTY_STRING = ""
    DEFAULT_EXIT_RESPONSE = "Bye!"
    DEFAULT_EXIT_RESPONSE_SRAI = ""
    DEFAULT_INITIAL_QUESTION = "Hello"
    DEFAULT_INITIAL_QUESTION_SRAI = ""
    DEFAULT_OVERRIDE_PREDICATES = True
    DEFAULT_MAX_QUESTION_RECURSION = 100
    DEFAULT_MAX_QUESTION_TIMEOUT = -1
    DEFAULT_MAX_SEARCH_DEPTH = 100
    DEFAULT_MAX_SEARCH_TIMEOUT = -1
    DEFAULT_TAB_PARSE_OUTPUT = True

    def __init__(self):
        self._license_keys = None
        self._bot_root = BotConfiguration.DEFAULT_ROOT
        self._prompt = BotConfiguration.DEFAULT_PROMPT
        self._default_response = BotConfiguration.DEFAULT_RESPONSE
        self._default_response_srai = BotConfiguration.DEFAULT_RESPONSE_SRAI
        self._exit_response = BotConfiguration.DEFAULT_EXIT_RESPONSE
        self._exit_response_srai = BotConfiguration.DEFAULT_EXIT_RESPONSE_SRAI
        self._initial_question = BotConfiguration.DEFAULT_INITIAL_QUESTION
        self._initial_question_srai = BotConfiguration.DEFAULT_INITIAL_QUESTION_SRAI
        self._empty_string = BotConfiguration.DEFAULT_EMPTY_STRING
        self._override_properties = BotConfiguration.DEFAULT_OVERRIDE_PREDICATES
        self._max_question_recursion = BotConfiguration.DEFAULT_MAX_QUESTION_RECURSION
        self._max_question_timeout = BotConfiguration.DEFAULT_MAX_QUESTION_TIMEOUT
        self._max_search_depth = BotConfiguration.DEFAULT_MAX_SEARCH_DEPTH
        self._max_search_timeout = BotConfiguration.DEFAULT_MAX_SEARCH_TIMEOUT
        self._tab_parse_output = BotConfiguration.DEFAULT_TAB_PARSE_OUTPUT
        self._spelling = BotSpellingConfiguration()
        self._conversations = BotConversationsConfiguration()
        BaseContainerConfigurationData.__init__(self, "bot")

    def load_configuration(self, configuration_file, bot_root):
        bot = configuration_file.get_section(self.section_name)
        if bot is not None:
            self._license_keys = self._get_file_option(configuration_file, "license_keys", bot, bot_root)
            self._prompt = configuration_file.get_option(bot, "prompt",
                                                         BotConfiguration.DEFAULT_PROMPT)
            self._default_response = configuration_file.get_option(bot, "default_response",
                                                                   BotConfiguration.DEFAULT_RESPONSE)
            self._default_response_srai = configuration_file.get_option(bot, "default_response_srai",
                                                                        BotConfiguration.DEFAULT_RESPONSE_SRAI)
            self._empty_string = configuration_file.get_option(bot, "empty_string",
                                                               BotConfiguration.DEFAULT_EMPTY_STRING)
            self._exit_response = configuration_file.get_option(bot, "exit_response",
                                                                BotConfiguration.DEFAULT_EXIT_RESPONSE)
            self._exit_response_srai = configuration_file.get_option(bot, "exit_response_srai",
                                                                     BotConfiguration.DEFAULT_EXIT_RESPONSE_SRAI)
            self._initial_question = configuration_file.get_option(bot, "initial_question",
                                                                   BotConfiguration.DEFAULT_INITIAL_QUESTION)
            self._initial_question_srai = configuration_file.get_option(bot, "initial_question_srai",
                                                                        BotConfiguration.DEFAULT_INITIAL_QUESTION_SRAI)
            self._override_properties = configuration_file.get_option(bot, "override_properties",
                                                                      BotConfiguration.DEFAULT_OVERRIDE_PREDICATES)
            self._max_question_recursion = configuration_file.get_int_option(bot, "max_question_recursion",
                                                                             BotConfiguration.DEFAULT_MAX_QUESTION_RECURSION)
            self._max_question_timeout = configuration_file.get_int_option(bot, "max_question_timeout",
                                                                           BotConfiguration.DEFAULT_MAX_QUESTION_TIMEOUT)
            self._max_search_depth = configuration_file.get_int_option(bot, "max_search_depth",
                                                                       BotConfiguration.DEFAULT_MAX_SEARCH_DEPTH)
            self._max_search_timeout = configuration_file.get_int_option(bot, "max_search_timeout",
                                                                         BotConfiguration.DEFAULT_MAX_SEARCH_TIMEOUT)
            self._tab_parse_output = configuration_file.get_bool_option(bot, "tab_parse_output",
                                                                        BotConfiguration.DEFAULT_TAB_PARSE_OUTPUT)

            self._spelling.load_config_section(configuration_file, bot, bot_root)
            self._conversations.load_config_section(configuration_file, bot, bot_root)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("Config section [%s] missing, using default values", self.section_name)

    @property
    def bot_root(self):
        return self._bot_root

    @property
    def license_keys(self):
        return self._license_keys

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, text):
        self._prompt = text

    @property
    def default_response(self):
        return self._default_response

    @default_response.setter
    def default_response(self, text):
        self._default_response = text

    @property
    def default_response_srai(self):
        return self._default_response_srai

    @default_response_srai.setter
    def default_response_srai(self, text):
        self._default_response_srai = text

    @property
    def empty_string(self):
        return self._empty_string

    @empty_string.setter
    def empty_string(self, text):
        self._empty_string = text

    @property
    def exit_response(self):
        return self._exit_response

    @exit_response.setter
    def exit_response(self, text):
        self._exit_response = text

    @property
    def exit_response_srai(self):
        return self._exit_response_srai

    @exit_response_srai.setter
    def exit_response_srai(self, text):
        self._exit_response_srai = text

    @property
    def initial_question(self):
        return self._initial_question

    @initial_question.setter
    def initial_question(self, text):
        self._initial_question = text

    @property
    def initial_question_srai(self):
        return self._initial_question_srai

    @initial_question_srai.setter
    def initial_question_srai(self, text):
        self._initial_question_srai = text

    @property
    def override_properties(self):
        return self._override_properties

    @override_properties.setter
    def override_properties(self, override):
        self._override_properties = override

    @property
    def max_question_recursion(self):
        return self._max_question_recursion

    @property
    def max_question_timeout(self):
        return self._max_question_timeout

    @property
    def max_search_depth(self):
        return self._max_search_depth

    @property
    def max_search_timeout(self):
        return self._max_search_timeout

    @property
    def tab_parse_output(self):
        return self._tab_parse_output

    @property
    def spelling(self):
        return self._spelling

    @property
    def conversations(self):
        return self._conversations
