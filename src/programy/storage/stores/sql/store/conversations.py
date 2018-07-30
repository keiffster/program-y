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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.conversation import ConversationStore
from programy.storage.stores.sql.dao.conversation import Conversation


class SQLConversationStore(SQLStore, ConversationStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(Conversation).delete()

    def store_conversation(self, clientid, userid, botid, brainid, depth, question, response):
        conversation = Conversation(clientid=clientid, userid=userid, botid=botid, brainid=brainid, question_depth=depth, question=question, response=response)
        self._storage_engine.session.add(conversation)
        return conversation

    def load_conversation(self, clientid, userid):
        db_conversations = self._storage_engine.session.query(Conversation).filter(Conversation.clientid==clientid, Conversation.userid==userid)
        conversations = []
        for conversation in db_conversations:
            conversations.append({"clientid": conversation.clientid, "userid": conversation.userid, "botid": conversation.botid, "brainid": conversation.brainid,
                                  "question_depth": conversation.question_depth, "question": conversation.question, "response": conversation.response})
        return conversations
