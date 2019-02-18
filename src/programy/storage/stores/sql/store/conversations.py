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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.conversation import ConversationStore
from programy.storage.stores.sql.dao.conversation import Conversation
from programy.dialog.question import Question
from programy.dialog.sentence import Sentence


class SQLConversationStore(SQLStore, ConversationStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(Conversation).delete()

    def store_conversation(self, client_context, conversation):
        question_no = 0
        for question in conversation.questions:
            sentence_no = 0
            for sentence in question.sentences:

                self._storage_engine.session.query(Conversation).filter(Conversation.clientid==client_context.client.id,
                                                                        Conversation.userid==client_context.userid,
                                                                        Conversation.botid==client_context.bot.id,
                                                                        Conversation.brainid==client_context.brain.id,
                                                                        Conversation.question==question_no).delete()

                conversation = Conversation(clientid=client_context.client.id,
                                            userid=client_context.userid,
                                            botid=client_context.bot.id,
                                            brainid=client_context.brain.id,
                                            question=question_no,
                                            sentence=sentence.text(),
                                            response=sentence.response)
                self._storage_engine.session.add(conversation)
                sentence_no += 1
                question_no += 1

    def load_conversation(self, client_context, conversation):
        db_conversations = self._storage_engine.session.query(Conversation).filter(Conversation.clientid==client_context.client.id, Conversation.userid==client_context.userid)
        question = Question()
        conversation.questions.append(question)

        current_question = 0
        for conversation in db_conversations:

            if conversation.question != current_question:
                question = Question ()
                conversation.questions.append(question)

            sentence = Sentence(client_context.bot.brain.tokenizer, conversation.sentence)
            sentence.response = conversation.response
            question.sentences.append(sentence)
