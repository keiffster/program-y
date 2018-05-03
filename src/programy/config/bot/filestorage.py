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

from programy.config.base import BaseConfigurationData

class BotConversationsFileStorageConfiguration(BaseConfigurationData):

    def __init__(self, config_name):
        BaseConfigurationData.__init__(self, name=config_name)
        self._dir = None

    @property
    def dir(self):
        return self._dir

    def load_config_section(self, configuration_file, configuration, bot_root):
        ConversationsFileStorage = configuration_file.get_section(self._section_name, configuration)
        if ConversationsFileStorage is not None:
            dir = configuration_file.get_option(ConversationsFileStorage, "dir", missing_value=None)
            if dir is not None:
                self._dir = self.sub_bot_root(dir, bot_root)
        else:
            YLogger.warning(self, "'BotConversationsFileStorageConfiguration' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['dir'] = './conversations'
        else:
            data['dir'] = self._dir