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

from programy.config.base import BaseConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BotSentenceJoinerConfiguration(BaseConfigurationData):

    DEFAULT_CLASSNAME = "programy.dialog.joiner.joiner.SentenceJoiner"
    DEFAULT_JOIN_CHARS = ".?!"
    DEFAULT_TERMINATOR = "."

    def __init__(self):
        BaseConfigurationData.__init__(self, name="joiner")
        self._classname = BotSentenceJoinerConfiguration.DEFAULT_CLASSNAME
        self._join_chars = BotSentenceJoinerConfiguration.DEFAULT_JOIN_CHARS
        self._terminator = BotSentenceJoinerConfiguration.DEFAULT_TERMINATOR

    @property
    def classname(self):
        return self._classname

    @property
    def join_chars(self):
        return self._join_chars

    @property
    def terminator(self):
        return self._terminator

    def check_for_license_keys(self, license_keys):
        BaseConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        joiner = configuration_file.get_section(self._section_name, configuration)
        if joiner is not None:
            self._classname = configuration_file.get_option(joiner, "classname", missing_value=BotSentenceJoinerConfiguration.DEFAULT_CLASSNAME, subs=subs)
            self._join_chars = configuration_file.get_option(joiner, "join_chars", missing_value=BotSentenceJoinerConfiguration.DEFAULT_JOIN_CHARS, subs=subs)
            self._terminator = configuration_file.get_option(joiner, "terminator", missing_value=BotSentenceJoinerConfiguration.DEFAULT_TERMINATOR, subs=subs)
        else:
            YLogger.warning(self, "'joiner' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = BotSentenceJoinerConfiguration.DEFAULT_CLASSNAME
            data['join_chars'] = BotSentenceJoinerConfiguration.DEFAULT_JOIN_CHARS
            data['terminator'] = BotSentenceJoinerConfiguration.DEFAULT_TERMINATOR
        else:
            data['classname'] = self._classname
            data['join_chars'] = self._join_chars
            data['terminator'] = self._terminator
