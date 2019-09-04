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

from sqlalchemy import Column, Integer, String, Boolean

from programy.storage.stores.sql.base import Base
from programy.storage.stores.utils import DAOUtils

from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.dialog.sentence import Sentence
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match as MatchObject


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)

    clientid = Column(String(16))
    userid = Column(String(16))
    botid = Column(String(16))
    brainid = Column(String(16))
    maxhistories = Column(Integer)

    def __repr__(self):
        return "<Conversation(id='%s', clientid='%s', userid='%s', botid='%s', brainid='%s', maxhistories='%d'>" % \
               (DAOUtils.valid_id(self.id),
                self.clientid,
                self.userid,
                self.botid,
                self.brainid,
                self.maxhistories)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)

    conversationid = Column(Integer)
    questionno = Column(Integer)
    srai = Column(Boolean)

    def __repr__(self):
        return "<Question(id='%s', conversationid='%d', questionno='%d', srai='%s'>" % \
               (DAOUtils.valid_id(self.id), self.conversationid, self.questionno, self.srai)


class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True)

    questionid = Column(Integer)
    sentenceno = Column(Integer)
    sentence = Column(String(256))
    response = Column(String(2000))
    positivity = Column(String(10))
    subjectivity = Column(String(10))

    def __repr__(self):
        return "<Sentence(id='%s', questionid='%d', sentenceno='%d', sentence='%s', response='%s', " \
               "positivity='%s', subjectivity='%s'>" % (DAOUtils.valid_id(self.id),
                                                                        self.questionid, self.sentenceno,
                                                                        self.sentence, self.response,
                                                                        self.positivity, self.subjectivity)


class ConversationProperty(Base):
    __tablename__ = 'conprops'

    CONVERSATION = 1
    QUESTION = 2

    id = Column(Integer, primary_key=True)

    conversationid = Column(Integer)
    questionid = Column(Integer)
    type = Column(Integer)
    name = Column(String(48))
    value = Column(String(256))

    def __repr__(self):
        return "<ConversationProperty(id='%s', conversationid='%d', questionid='%d', " \
               "type='%d', name='%s', value='%s')>" % \
               (DAOUtils.valid_id(self.id), self.conversationid, self.questionid,
                self.type, self.name, self.value)


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)

    sentenceid = Column(Integer)

    max_search_depth = Column(Integer())
    max_search_timeout = Column(Integer())
    sentence = Column(String(256))
    response = Column(String(500))

    score = Column(String(20))

    def __repr__(self):
        return "<Match(id='%s', max_search_depth='%d', max_search_timeout='%d', " \
               "sentence='%s', response='%s', score='%s')>" % \
               (DAOUtils.valid_id(self.id), self.max_search_depth, self.max_search_timeout,
                self.sentence, self.response, self.score)


class MatchNode(Base):
    __tablename__ = 'matchednodes'

    id = Column(Integer, primary_key=True)

    matchid = Column(Integer)
    matchcount = Column(Integer)
    matchtype = Column(String(10))
    matchnode = Column(String(256))
    matchstr = Column(String(256))
    wildcard = Column(Boolean)
    multiword = Column(Boolean)

    def __repr__(self):
        return "<MatchNode(id='%s', matchid='%d', matchcount='%d', matchtype='%s'," \
               " matchnode='%s', matchstr='%s', wildcard='%s', multiword='%s')>" % \
               (DAOUtils.valid_id(self.id), self.matchid, self.matchcount, self.matchtype,
                self.matchnode, self.matchstr, self.wildcard, self.multiword)
