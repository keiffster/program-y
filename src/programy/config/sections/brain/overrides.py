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

class BrainOverridesConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "overrides")
        self._allow_system_aiml = False
        self._allow_learn_aiml = False
        self._allow_learnf_aiml = False

    @property
    def allow_system_aiml(self):
        return self._allow_system_aiml

    @property
    def allow_learn_aiml(self):
        return self._allow_learn_aiml

    @property
    def allow_learnf_aiml(self):
        return self._allow_learnf_aiml

    def load_config_section(self, file_config, bot_config, bot_root):
        overrides = file_config.get_section("overrides", bot_config)
        if overrides is not None:
            self._allow_system_aiml = file_config.get_option(overrides, "allow_system_aiml", missing_value=None)
            self._allow_learn_aiml = file_config.get_option(overrides, "allow_learn_aiml", missing_value=None)
            self._allow_learnf_aiml = file_config.get_option(overrides, "allow_learnf_aiml", missing_value=None)
        else:
            logging.warning("'overrides' section missing from brain config, using to defaults")
