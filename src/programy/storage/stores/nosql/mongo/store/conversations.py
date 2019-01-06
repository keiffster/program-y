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
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.conversation import ConversationStore
from programy.storage.stores.nosql.mongo.dao.conversation import Conversation


class MongoConversationStore(MongoStore, ConversationStore):

    CONVERSATIONS = 'conversations'
    CONVERSATION = 'conversation'
    CLIENITD = 'clientid'
    USERID = 'userid'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoConversationStore.CONVERSATIONS

    def store_conversation(self, client_context, conversation):
        YLogger.info(client_context, "Storing conversation to Mongo [%s] [%s]", client_context.client.id, client_context.userid)
        return self.add_document(Conversation(client_context, conversation))

    def load_conversation(self, client_context, conversation):
        YLogger.info(client_context, "Loading conversation from Mongo [%s] [%s]", client_context.client.id, client_context.userid)
        collection = self.collection()
        document = collection.find_one({MongoConversationStore.CLIENITD: client_context.client.id,
                                        MongoConversationStore.USERID: client_context.userid})
        if document:
            data = document
            conversation.from_json(client_context, data[MongoConversationStore.CONVERSATION])
            return True
        return False