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

from programy.config.container import BaseContainerConfigurationData
from programy.config.brain.brain import BrainConfiguration
from programy.config.bot.spelling import BotSpellingConfiguration
from programy.config.bot.conversations import BotConversationsConfiguration
from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.config.bot.joiner import BotSentenceJoinerConfiguration
from programy.config.bot.translation import BotTranslatorConfiguration
from programy.config.bot.sentiment import BotSentimentAnalyserConfiguration
from programy.utils.substitutions.substitues import Substitutions


class BotConfiguration(BaseContainerConfigurationData):

    DEFAULT_ROOT = "."
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

    def __init__(self, section_name="bot"):

        self._brain_configs = []
        self._brain_configs.append(BrainConfiguration("brain"))
        self._brain_selector = None

        self._bot_root = BotConfiguration.DEFAULT_ROOT
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
        self._from_translator = BotTranslatorConfiguration(name="from_translator")
        self._to_translator = BotTranslatorConfiguration(name="to_translator")
        self._sentiment = BotSentimentAnalyserConfiguration()
        self._conversations = BotConversationsConfiguration()
        self._splitter = BotSentenceSplitterConfiguration()
        self._joiner = BotSentenceJoinerConfiguration()
        BaseContainerConfigurationData.__init__(self, section_name)

    def check_for_license_keys(self, license_keys):
        BaseContainerConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration(self, configuration_file, bot_root, subs: Substitutions = None):
        bot = configuration_file.get_section(self.section_name)
        if bot is not None:

            self._default_response = configuration_file.get_option(bot, "default_response",
                                                                   BotConfiguration.DEFAULT_RESPONSE, subs=subs)
            self._default_response_srai = configuration_file.get_option(bot, "default_response_srai",
                                                                        BotConfiguration.DEFAULT_RESPONSE_SRAI, subs=subs)
            self._empty_string = configuration_file.get_option(bot, "empty_string",
                                                               BotConfiguration.DEFAULT_EMPTY_STRING, subs=subs)
            self._exit_response = configuration_file.get_option(bot, "exit_response",
                                                                BotConfiguration.DEFAULT_EXIT_RESPONSE, subs=subs)
            self._exit_response_srai = configuration_file.get_option(bot, "exit_response_srai",
                                                                     BotConfiguration.DEFAULT_EXIT_RESPONSE_SRAI, subs=subs)
            self._initial_question = configuration_file.get_option(bot, "initial_question",
                                                                   BotConfiguration.DEFAULT_INITIAL_QUESTION, subs=subs)
            self._initial_question_srai = configuration_file.get_option(bot, "initial_question_srai",
                                                                        BotConfiguration.DEFAULT_INITIAL_QUESTION_SRAI, subs=subs)
            self._override_properties = configuration_file.get_option(bot, "override_properties",
                                                                      BotConfiguration.DEFAULT_OVERRIDE_PREDICATES, subs=subs)
            self._max_question_recursion = configuration_file.get_int_option(bot, "max_question_recursion",
                                                                             BotConfiguration.DEFAULT_MAX_QUESTION_RECURSION, subs=subs)
            self._max_question_timeout = configuration_file.get_int_option(bot, "max_question_timeout",
                                                                           BotConfiguration.DEFAULT_MAX_QUESTION_TIMEOUT, subs=subs)
            self._max_search_depth = configuration_file.get_int_option(bot, "max_search_depth",
                                                                       BotConfiguration.DEFAULT_MAX_SEARCH_DEPTH, subs=subs)
            self._max_search_timeout = configuration_file.get_int_option(bot, "max_search_timeout",
                                                                         BotConfiguration.DEFAULT_MAX_SEARCH_TIMEOUT, subs=subs)
            self._tab_parse_output = configuration_file.get_bool_option(bot, "tab_parse_output",
                                                                        BotConfiguration.DEFAULT_TAB_PARSE_OUTPUT, subs=subs)

            self._spelling.load_config_section(configuration_file, bot, bot_root, subs=subs)

            self._conversations.load_config_section(configuration_file, bot, bot_root, subs=subs)

            self._splitter.load_config_section(configuration_file, bot, bot_root, subs=subs)

            self._joiner.load_config_section(configuration_file, bot, bot_root, subs=subs)

            self._from_translator.load_config_section(configuration_file, bot, bot_root, subs=subs)

            self._to_translator.load_config_section(configuration_file, bot, bot_root, subs=subs)

            self._sentiment.load_config_section(configuration_file, bot, bot_root, subs=subs)

        else:
            YLogger.warning(self, "Config section [%s] missing, using default values", self.section_name)

        self.load_configurations(configuration_file, bot, bot_root, subs)

    def load_configurations(self, configuration_file, bot, bot_root, subs: Substitutions = None):
        if bot is not None:
            brain_names = configuration_file.get_multi_option(bot, "brain", missing_value="brain")
            first = True
            for name in brain_names:
                if first is True:
                    config = self._brain_configs[0]
                    first = False
                else:
                    config = BrainConfiguration(name)
                    self._brain_configs.append(config)
                config.load_configuration(configuration_file, bot_root, subs=subs)

                self._brain_selector = configuration_file.get_option(bot, "brain_selector", subs=subs)

        else:
            YLogger.warning(self, "No brain name defined for bot [%s], defaulting to 'brain'.", self.section_name)
            brain_name = "brain"
            self._brain_configs[0]._section_name = brain_name
            self._brain_configs[0].load_configuration(configuration_file, bot_root, subs=subs)

    @property
    def configurations(self):
        return self._brain_configs

    @property
    def brain_selector(self):
        return self._brain_selector

    @property
    def bot_root(self):
        return self._bot_root

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

    @property
    def splitter(self):
        return self._splitter

    @property
    def joiner(self):
        return self._joiner

    @property
    def from_translator(self):
        return self._from_translator

    @property
    def to_translator(self):
        return self._to_translator

    @property
    def sentiment_analyser(self):
        return self._sentiment

    def to_yaml(self, data, defaults=True):

        data['bot_root'] = self.bot_root
        data['default_response'] = self.default_response
        data['default_response_srai'] = self.default_response_srai
        data['exit_response'] = self.exit_response
        data['exit_response_srai'] = self.exit_response_srai
        data['initial_question'] = self.initial_question
        data['initial_question_srai'] = self.initial_question_srai
        data['empty_string'] = self.empty_string
        data['override_properties'] = self.override_properties
        data['max_question_recursion'] = self.max_question_recursion
        data['max_question_timeout'] = self.max_question_timeout
        data['max_search_depth'] = self.max_search_depth
        data['max_search_timeout'] = self.max_search_timeout
        data['tab_parse_output'] = self.tab_parse_output
        self.config_to_yaml(data, BotSpellingConfiguration(), defaults)
        self.config_to_yaml(data, BotConversationsConfiguration(), defaults)
        self.config_to_yaml(data, BotSentenceSplitterConfiguration(), defaults)
        self.config_to_yaml(data, BotSentenceJoinerConfiguration(), defaults)
        self.config_to_yaml(data, BotTranslatorConfiguration(name="from_translator"), defaults)
        self.config_to_yaml(data, BotTranslatorConfiguration(name="to_translator"), defaults)
        self.config_to_yaml(data, BotSentimentAnalyserConfiguration(), defaults)
