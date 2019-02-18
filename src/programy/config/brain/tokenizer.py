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


class BrainTokenizerConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="tokenizer")
        self._classname = None
        self._split_chars = " "

    @property
    def classname(self):
        return self._classname

    @property
    def split_chars(self):
        return self._split_chars

    def check_for_license_keys(self, license_keys):
        BaseConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        tokenizer = configuration_file.get_section(self._section_name, configuration)
        if tokenizer is not None:
            self._classname = configuration_file.get_option(tokenizer, "classname", missing_value="programy.parser.tokenizer.Tokenizer", subs=subs)
            self._split_chars = configuration_file.get_option(tokenizer, "split_chars", missing_value=" ", subs=subs)
        else:
            YLogger.warning(self, "'tokenizer' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = "programy.parser.tokenizer.Tokenizer"
            data['split_chars'] = ' '
        else:
            data['classname'] = self._classname
            data['split_chars'] = self._split_chars
