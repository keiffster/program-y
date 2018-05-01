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
import os

from programy.config.section import BaseSectionConfigurationData


class BrainDefaultsConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "defaults")
        self._default_get = "unknown"
        self._default_property = "unknown"
        self._default_map = "unknown"
        if os.name == 'posix':
            self._learnf_path = '/tmp/learnf'
        elif os.name == 'nt':
            self._learnf_path = 'C:\\Windows\\Temp\\leanf'

    @property
    def default_get(self):
        return self._default_get

    @property
    def default_property(self):
        return self._default_property

    @property
    def default_map(self):
        return self._default_map

    @property
    def learnf_path(self):
        return self._learnf_path

    def load_config_section(self, configuration_file, configuration, bot_root):
        binaries = configuration_file.get_section("defaults", configuration)
        if binaries is not None:
            self._default_get = configuration_file.get_option(binaries, "default-get", missing_value=None)
            self._default_property = configuration_file.get_option(binaries, "default-property", missing_value=None)
            self._default_map = configuration_file.get_option(binaries, "default-map", missing_value=None)
            learnf_path = configuration_file.get_option(binaries, "learnf-path", missing_value=None)
            if learnf_path is not None:
                self._learnf_path = self.sub_bot_root(learnf_path, bot_root)
        else:
            YLogger.warning(self, "'defaults' section missing from bot config, using default defaults")
