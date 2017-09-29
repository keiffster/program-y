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

from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration


class ProgramyConfiguration(object):

    def __init__(self, client_configuration, brain_config=None, bot_config=None):
        if brain_config is None:
            self._brain_config = BrainConfiguration()
        else:
            self._brain_config = brain_config

        if bot_config is None:
            self._bot_config = BotConfiguration()
        else:
            self._bot_config = bot_config

        self._client_config = client_configuration

    @property
    def brain_configuration(self):
        return self._brain_config

    @property
    def bot_configuration(self):
        return self._bot_config

    @property
    def client_configuration(self):
        return self._client_config

    def load_config_data(self, config_file, bot_root):
        self._brain_config.load_configuration(config_file, bot_root)
        self._bot_config.load_configuration(config_file, bot_root)
        self._client_config.load_configuration(config_file, bot_root)
