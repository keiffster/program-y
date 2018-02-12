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

from programy.config.base import BaseConfigurationData

class BotConversationsRedisStorageConfiguration(BaseConfigurationData):

    def __init__(self, config_name):
        BaseConfigurationData.__init__(self, name=config_name)
        self._host = None
        self._port = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def load_config_section(self, configuration_file, configuration, bot_root):
        ConversationsFileStorage = configuration_file.get_section(self._section_name, configuration)
        if ConversationsFileStorage is not None:
            self._host = configuration_file.get_option(ConversationsFileStorage, "host", missing_value="localhost")
            self._port = configuration_file.get_int_option(ConversationsFileStorage, "port", missing_value=6379)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("'BotConversationsRedisStorageConfiguration' section missing from bot config, using defaults")
