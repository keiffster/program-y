"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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


class BrainBinariesConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "binaries")
        self._save_binary = False
        self._load_binary = False
        self._binary_filename = None
        self._load_aiml_on_binary_fail = False
        self._dump_to_file = None

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

    @property
    def dump_to_file(self):
        return self._dump_to_file

    def load_config_section(self, file_config, bot_config, bot_root):
        binaries = file_config.get_section("binaries", bot_config)
        if binaries is not None:
            self._save_binary = file_config.get_option(binaries, "save_binary", missing_value=None)
            self._load_binary = file_config.get_option(binaries, "load_binary", missing_value=None)
            binary_filename = file_config.get_option(binaries, "binary_filename", missing_value=None)
            if binary_filename is not None:
               self._binary_filename = self.sub_bot_root(binary_filename, bot_root)
            self._load_aiml_on_binary_fail = file_config.get_option(binaries, "load_aiml_on_binary_fail", missing_value=None)
            dump_to_file = file_config.get_option(binaries, "dump_to_file", missing_value=None)
            if dump_to_file is not None:
                self._dump_to_file = self.sub_bot_root(dump_to_file, bot_root)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING): logging.warning("'binaries' section missing from bot config, using to defaults")