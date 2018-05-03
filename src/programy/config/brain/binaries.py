"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from programy.config.section import BaseSectionConfigurationData


class BrainBinariesConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "binaries")
        self._save_binary = False
        self._load_binary = False
        self._binary_filename = None
        self._load_aiml_on_binary_fail = False

    @property
    def save_binary(self):
        return self._save_binary

    @property
    def load_binary(self):
        return self._load_binary

    @property
    def binary_filename(self):
        return self._binary_filename

    @property
    def load_aiml_on_binary_fail(self):
        return self._load_aiml_on_binary_fail

    def load_config_section(self, configuration_file, configuration, bot_root):
        binaries = configuration_file.get_section("binaries", configuration)
        if binaries is not None:
            self._save_binary = configuration_file.get_option(binaries, "save_binary", missing_value=None)
            self._load_binary = configuration_file.get_option(binaries, "load_binary", missing_value=None)
            binary_filename = configuration_file.get_option(binaries, "binary_filename", missing_value=None)
            if binary_filename is not None:
                self._binary_filename = self.sub_bot_root(binary_filename, bot_root)
            self._load_aiml_on_binary_fail = configuration_file.get_option(binaries, "load_aiml_on_binary_fail", missing_value=None)
        else:
            YLogger.warning(self, "'binaries' section missing from bot config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['save_binary'] = False
            data['load_binary'] = False
            data['binary_filename'] = "./braintree.bin"
            data['load_aiml_on_binary_fail'] = True
        else:
            data['save_binary'] = self._save_binary
            data['load_binary'] = self._load_binary
            data['binary_filename'] = self._binary_filename
            data['load_aiml_on_binary_fail'] = self._load_aiml_on_binary_fail
