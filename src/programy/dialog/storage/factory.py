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

from programy.config.bot.filestorage import BotConversationsFileStorageConfiguration
from programy.config.bot.redisstorage import BotConversationsRedisStorageConfiguration
from programy.dialog.storage.file import ConversationFileStorage
from programy.dialog.storage.redis import ConversationRedisStorage

class ConversationStorageFactory(object):

    @staticmethod
    def get_storage_config(type, config_name, configuration_file, configuration, bot_root):
        if type == 'file':
            storage = BotConversationsFileStorageConfiguration(config_name=config_name)
            storage.load_config_section(configuration_file, configuration, bot_root)
            return storage
        elif type == 'redis':
            storage = BotConversationsRedisStorageConfiguration(config_name=config_name)
            storage.load_config_section(configuration_file, configuration, bot_root)
            return storage

        YLogger.warning(None, "Invalid Conversations file storage type [%s]", type)
        return None

    @staticmethod
    def get_storage(config):

        if config.conversations.type == 'file':
            return ConversationFileStorage(config.conversations.storage)
        elif config.conversations.type == 'redis':
            return ConversationRedisStorage(config.conversations.storage)

        YLogger.warning(None, "Invalid Conversations file storage type [%s]", config.conversations.type)
        return None
