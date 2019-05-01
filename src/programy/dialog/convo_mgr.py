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
from programy.dialog.conversation import Conversation
from programy.storage.factory import StorageFactory
from programy.config.bot.conversations import BotConversationsConfiguration


class ConversationManager(object):

    def __init__(self, conversation_configuration):
        assert (conversation_configuration is not None)
        assert (isinstance(conversation_configuration, BotConversationsConfiguration))

        self._configuration = conversation_configuration
        self._conversation_storage = None
        self._conversations = {}

    @property
    def configuration(self):
        return self._configuration

    @property
    def storage(self):
        return self._conversation_storage

    @property
    def conversations(self):
        return self._conversations

    def empty(self):
        self._conversations.clear()

    def initialise(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.CONVERSATIONS) is True:
            converstion_engine =  storage_factory.entity_storage_engine(StorageFactory.CONVERSATIONS)
            if converstion_engine:
                self._conversation_storage = converstion_engine.conversation_store()

    def save_conversation(self, client_context):
        if self._conversation_storage is not None:
            if client_context.userid in self._conversations:
                conversation = self._conversations[client_context.userid]
                if conversation is not None:
                    self._conversation_storage.store_conversation(client_context, conversation)

    def has_conversation(self, client_context):
        return bool(client_context.userid in self._conversations)

    def get_conversation(self, client_context):

        assert (client_context is not None)
        assert (client_context.userid  is not None)

        if client_context.userid in self._conversations:
            YLogger.debug(client_context, "Retrieving conversation for client %s", client_context.userid)
            conversation = self._conversations[client_context.userid]

            # Load existing conversation from cache
            if self.configuration.multi_client:
                if self._conversation_storage is not None:
                    self._conversation_storage.load_conversation(client_context, conversation)

        else:
            YLogger.info(client_context, "Creating new conversation for client %s", client_context.userid)

            conversation = Conversation(client_context)

            if client_context.brain.default_variables is not None:
                conversation.load_initial_variables(client_context.brain.default_variables)

            self._conversations[client_context.userid] = conversation

            if self._conversation_storage is not None:
                self._conversation_storage.load_conversation(client_context, conversation)

            if self.configuration.restore_last_topic is True:
                pass

        return conversation

