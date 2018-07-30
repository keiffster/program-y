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
from programy.dialog.storage.factory import ConversationStorageFactory

class BotConversationsConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="conversations")
        self._save = False
        self._load = False
        self._max_histories = 100
        self._restore_last_topic = False
        self._initial_topic = "*"
        self._empty_on_start = False

    @property
    def save(self):
        return self._save

    @property
    def load(self):
        return self._load

    @property
    def max_histories(self):
        return self._max_histories

    @property
    def initial_topic(self):
        return self._initial_topic

    @property
    def restore_last_topic(self):
        return self._restore_last_topic

    @property
    def empty_on_start(self):
        return self._empty_on_start

    def load_config_section(self, configuration_file, configuration, bot_root):
        Conversations = configuration_file.get_section(self._section_name, configuration)
        if Conversations is not None:
            self._save = configuration_file.get_bool_option(Conversations, "save", missing_value=True)
            self._load = configuration_file.get_bool_option(Conversations, "load", missing_value=False)
            self._max_histories = configuration_file.get_int_option(Conversations, "max_histories", missing_value=100)
            self._initial_topic = configuration_file.get_option(Conversations, "initial_topic", missing_value="*")
            self._restore_last_topic = configuration_file.get_bool_option(Conversations, "restore_last_topic", missing_value=False)
            self._empty_on_start = configuration_file.get_bool_option(Conversations, "empty_on_start", missing_value=False)
        else:
            YLogger.warning(self, "'Conversations' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['save'] = True
            data['load'] = False
            data['max_histories'] = 100
            data['restore_last_topic'] = True
            data['initial_topic'] = "*"
            data['empty_on_start'] = True
        else:
            data['save'] = self._save
            data['load'] = self._load
            data['max_histories'] = self._max_histories
            data['restore_last_topic'] = self._restore_last_topic
            data['initial_topic'] = self._initial_topic
            data['empty_on_start'] = self._empty_on_start
