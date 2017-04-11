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
from programy.config.base import BaseConfigurationData


class BotConfiguration(BaseConfigurationData):

    DEFAULT_ROOT                    = "."
    DEFAULT_PROMPT                  = ">>> "
    DEFAULT_RESPONSE                = "Sorry, I don't have an answer for that right now"
    DEFAULT_EXIT_RESPONSE          = "Bye!"
    DEFAULT_INITIAL_QUESTION       = "Hello"
    DEFAULT_OVERRIDE_PREDICATES    = True

    def __init__(self):
        self.bot_root               = BotConfiguration.DEFAULT_ROOT
        self._prompt                = BotConfiguration.DEFAULT_PROMPT
        self._default_response      = BotConfiguration.DEFAULT_RESPONSE
        self._exit_response         = BotConfiguration.DEFAULT_EXIT_RESPONSE
        self._initial_question      = BotConfiguration.DEFAULT_INITIAL_QUESTION
        self._override_predicates   = BotConfiguration.DEFAULT_OVERRIDE_PREDICATES
        BaseConfigurationData.__init__(self, "bot")

    def load_config_section(self, config_file, bot_root):
        bot = config_file.get_section(self.section_name)
        if bot is not None:
            self._prompt = config_file.get_option(bot, "prompt", BotConfiguration.DEFAULT_PROMPT)
            self._default_response = config_file.get_option(bot, "default_response", BotConfiguration.DEFAULT_RESPONSE)
            self._exit_response = config_file.get_option(bot, "exit_response", BotConfiguration.DEFAULT_EXIT_RESPONSE)
            self._initial_question = config_file.get_option(bot, "initial_question", BotConfiguration.DEFAULT_INITIAL_QUESTION)
            self._override_predicates = config_file.get_option(bot, "override_predicates", BotConfiguration.DEFAULT_OVERRIDE_PREDICATES)
        else:
            logging.warning("Config section [%s] missing, using default values", self.section_name)
            self.bot_root               = BotConfiguration.DEFAULT_ROOT
            self._prompt                = BotConfiguration.DEFAULT_PROMPT
            self._default_response      = BotConfiguration.DEFAULT_RESPONSE
            self._exit_response         = BotConfiguration.DEFAULT_EXIT_RESPONSE
            self._initial_question      = BotConfiguration.DEFAULT_INITIAL_QUESTION
            self._override_predicates   = BotConfiguration.DEFAULT_OVERRIDE_PREDICATES

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
    def exit_response(self):
        return self._exit_response

    @exit_response.setter
    def exit_response(self, text):
        self._exit_response = text

    @property
    def initial_question(self):
        return self._initial_question

    @initial_question.setter
    def initial_question(self, text):
        self._initial_question = text

    @property
    def override_predicates(self):
        return self._override_predicates

    @override_predicates.setter
    def override_predicates(self, override):
        self._override_predicates = override

