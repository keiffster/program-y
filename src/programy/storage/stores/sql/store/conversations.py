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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.conversation import ConversationStore
from programy.storage.stores.sql.dao.conversation import Conversation as ConversationDAO
from programy.storage.stores.sql.dao.conversation import Question as QuestionDAO
from programy.storage.stores.sql.dao.conversation import Sentence as SentenceDAO
from programy.storage.stores.sql.dao.conversation import ConversationProperty as ConversationPropertyDAO
from programy.storage.stores.sql.dao.conversation import Match as MatchDAO
from programy.storage.stores.sql.dao.conversation import MatchNode as MatchNodeDAO
from programy.dialog.question import Question
from programy.dialog.sentence import Sentence
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext


class SQLConversationStore(SQLStore, ConversationStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(ConversationDAO).delete()

    def store_conversation(self, client_context, conversation, commit=True):

        YLogger.debug(client_context, "Storing Conversation....")
        conversationdao = self._storage_engine.session.query(ConversationDAO).\
                                        filter(ConversationDAO.clientid==client_context.client.id,
                                               ConversationDAO.userid==client_context.userid,
                                               ConversationDAO.botid==client_context.bot.id,
                                               ConversationDAO.brainid==client_context.brain.id).first()
        if conversationdao is None:
            conversationdao = ConversationDAO(clientid=client_context.client.id,
                                              userid=client_context.userid,
                                              botid=client_context.bot.id,
                                              brainid=client_context.brain.id,
                                              maxhistories=conversation.max_histories)

            self._storage_engine.session.add(conversationdao)
            self._storage_engine.session.flush()
            YLogger.debug(client_context, "Wrote conversation %s", conversationdao)
        else:
            YLogger.debug(client_context, "Conversation already exists, %s", conversationdao)

        self._write_properties_to_db(client_context,
                                     conversationdao.id, 0,
                                     ConversationPropertyDAO.CONVERSATION,
                                     conversation.properties)

        self._write_questions_to_db(client_context, conversationdao.id, conversation)

        if commit is True:
            self.commit()

    def _write_questions_to_db(self, client_context, conversationid, conversation):
        question_no = 1
        for question in conversation.questions:
            self._write_question_to_db(client_context, conversationid, question, question_no)
            question_no += 1
        self._storage_engine.session.flush()

    def _write_question_to_db(self, client_context, conversationid, question, question_no):

        questiondao = self._storage_engine.session.query(QuestionDAO).\
                                        filter(QuestionDAO.conversationid==conversationid,
                                               QuestionDAO.questionno==question_no).first()

        if questiondao is None:
            questiondao = QuestionDAO(
                conversationid=conversationid,
                questionno=question_no,
                srai=question.srai
            )

            self._storage_engine.session.add(questiondao)
            self._storage_engine.session.flush()
            YLogger.debug(client_context, "Writing question %s", questiondao)
        else:
            YLogger.debug(client_context, "Question already exists, %s", questiondao)

        self._write_properties_to_db(client_context,
                                     conversationid, questiondao.id,
                                     ConversationPropertyDAO.QUESTION,
                                     question.properties)

        self._write_sentences_to_db(client_context, questiondao.id, question)


    def _write_sentences_to_db(self, client_context, questionid, question):
        sentence_no = 1
        for sentence in question.sentences:
            self._write_sentence_to_db(client_context, questionid, sentence, sentence_no)
            sentence_no += 1
        self._storage_engine.session.flush()

    def _write_sentence_to_db(self, client_context, questionid, sentence, sentence_no):

        sentencedao = self._storage_engine.session.query(SentenceDAO).\
                                                filter(SentenceDAO.questionid==questionid,
                                                       SentenceDAO.sentenceno==sentence_no).first()

        if sentencedao is None:
            sentencedao = SentenceDAO(questionid=questionid,
                                      sentenceno=sentence_no,
                                      sentence=sentence.text(client_context),
                                      response=sentence.response,
                                      subjectivity=sentence.subjectivity,
                                      positivity=sentence.positivity)

            self._storage_engine.session.add(sentencedao)
            self._storage_engine.session.flush()
            YLogger.debug(client_context, "Writing sentence %s", sentencedao)
        else:
            YLogger.debug(client_context, "Sentence already exists, %s", sentencedao)

        if sentence.matched_context is not None:
            self._write_match_context_to_db(client_context, sentencedao.id, sentence.matched_context)

    def _write_match_context_to_db(self, client_context, sentenceid, matched_context):

        matchdao = self._storage_engine.session.query(MatchDAO). \
            filter(MatchDAO.sentenceid == sentenceid).first()

        if matchdao is None:
            matchdao = MatchDAO(sentenceid=sentenceid,
                                max_search_depth=matched_context._max_search_depth,
                                max_search_timeout=matched_context._max_search_timeout,
                                sentence=matched_context.sentence,
                                response=matched_context.response,
                                score=matched_context.calculate_match_score())

            self._storage_engine.session.add(matchdao)
            self._storage_engine.session.flush()
            YLogger.debug(client_context, "Writing match %s", matchdao)
        else:
            YLogger.debug(client_context, "Match already exists %s", matchdao)

        self._write_matches_to_db(client_context, matched_context, matchdao.id)

    def _write_matches_to_db(self, client_context, matched_context, matchid):
        match_count = 1
        for match in matched_context.matched_nodes:
            matchnodedao = self._storage_engine.session.query(MatchNodeDAO). \
                filter(MatchNodeDAO.matchid == matchid,
                       MatchNodeDAO.matchcount == match_count).first()

            if matchnodedao is None:
                matchnodedao = MatchNodeDAO(matchid=matchid,
                                            matchcount=match_count,
                                            matchtype=Match.type_to_string(match.matched_node_type),
                                            matchnode=match.matched_node_str,
                                            matchstr=match.joined_words(client_context),
                                            wildcard=match.matched_node_wildcard,
                                            multiword=match.matched_node_multi_word)

                self._storage_engine.session.add(matchnodedao)
                YLogger.debug(client_context, "Writing matched node %s", matchnodedao)

            else:
                YLogger.debug(client_context, "Matched node already exists, %s", matchnodedao)

            match_count += 1

    def _write_properties_to_db(self, client_context, conversationid, questionid, type, properties):
        for name, value in properties.items():
            propertydao = self._storage_engine.session.query(ConversationPropertyDAO). \
                filter(ConversationPropertyDAO.conversationid == conversationid,
                       ConversationPropertyDAO.questionid == questionid,
                       ConversationPropertyDAO.type == type,
                       ConversationPropertyDAO.name == name).first()

            if propertydao is None:
                propertydao = ConversationPropertyDAO(conversationid=conversationid,
                                                      questionid=questionid,
                                                      type=type,
                                                      name=name,
                                                      value=value)

                self._storage_engine.session.add(propertydao)
                self._storage_engine.session.flush()
                YLogger.debug(client_context, "Writing property %s", propertydao)

            elif propertydao.value != value:
                propertydao.value=value
                self._storage_engine.session.flush()
                YLogger.debug(client_context, "Updating property %s", propertydao)
            else:
                YLogger.debug(client_context, "Property already exists, %s", propertydao)

    def load_conversation(self, client_context, conversation):

        YLogger.debug(client_context, "Loading conversation")
        conversationdao = self._storage_engine.session.query(ConversationDAO).\
                                        filter(ConversationDAO.clientid==client_context.client.id,
                                               ConversationDAO.userid==client_context.userid,
                                               ConversationDAO.botid==client_context.bot.id,
                                               ConversationDAO.brainid==client_context.brain.id).first()

        if conversationdao is None:
            YLogger.debug(client_context, "No matching conversation in database")
            return

            YLogger.debug(client_context, "Loaded conversation %s", conversationdao)

        conversation._max_histories = conversationdao.maxhistories

        self._read_properties_from_db(client_context,
                                      conversationdao.id, 0,
                                      ConversationPropertyDAO.CONVERSATION, conversation.properties)

        self._read_questions_from_db(client_context,
                                     conversationdao.id,
                                     conversation)

    def _read_questions_from_db(self, client_context, conversationid, conversation):
        questiondaos = self._storage_engine.session.query(QuestionDAO).\
                            filter(QuestionDAO.conversationid==conversationid)

        for questiondao in questiondaos:
            YLogger.debug(client_context, "Loading question %s", questiondao)

            question = Question(questiondao.srai)

            self._read_properties_from_db(client_context, conversationid, questiondao.id, ConversationPropertyDAO.QUESTION,
                                          question.properties)

            self._read_sentences_from_db(client_context, questiondao.id, question)

            conversation.record_dialog(question)

    def _read_sentences_from_db(self, client_context, questiondid, question ):
        sentencedaos = self._storage_engine.session.query(SentenceDAO).\
                            filter(SentenceDAO.questionid==questiondid)

        for sentencedao in sentencedaos:
            YLogger.debug(client_context, "Loading sentence %s", sentencedao)

            sentence = Sentence(client_context, sentencedao.sentence)

            sentence._response = sentencedao.response
            sentence._positivity = float(sentencedao.positivity)
            sentence._subjectivity = float(sentencedao.subjectivity)
            sentence._matched_context = MatchContext(0,0)

            question.sentences.append(sentence)

            self._read_match_context_from_db(client_context, sentencedao.id, sentence._matched_context)

    def _read_match_context_from_db(self, client_context, sentenceid, matched_context):
        matchdao = self._storage_engine.session.query(MatchDAO).\
            filter(MatchDAO.sentenceid == sentenceid).first()

        if matchdao is not None:
            matched_context._matched_context = matchdao.max_search_depth
            matched_context._max_search_timeout = matchdao.max_search_timeout
            matched_context.sentence = matchdao.sentence
            matched_context.response = matchdao.response

            YLogger.debug(client_context, "Loading match context %s", matchdao)
            self._read_matches_from_db(client_context, matched_context, matchdao.id)

    def _read_matches_from_db(self, client_context, matched_context, matchid):
        matchnodedaos = self._storage_engine.session.query(MatchNodeDAO). \
            filter(MatchNodeDAO.matchid == matchid)

        for matchnodedao in matchnodedaos:
            YLogger.debug(client_context, "Loading match node %s", matchnodedao)

            match = Match(None, None, None)
            match._matched_node_type = Match.string_to_type(matchnodedao.matchtype)
            match._matched_node_str = matchnodedao.matchnode
            match._matched_node_words = client_context.brain.tokenizer.texts_to_words(matchnodedao.matchstr)
            match._matched_node_multi_word = matchnodedao.multiword

            matched_context.matched_nodes.append(match)

    def _read_properties_from_db(self, client_context, conversationid, questionid, type, properties):

        propertydaos = self._storage_engine.session.query(ConversationPropertyDAO). \
            filter(ConversationPropertyDAO.conversationid == conversationid,
                   ConversationPropertyDAO.questionid == questionid,
                   ConversationPropertyDAO.type == type)

        for propertydao in propertydaos:
            YLogger.debug(client_context, "Loading conversation property %s", propertydao)
            properties[propertydao.name] = propertydao.value

