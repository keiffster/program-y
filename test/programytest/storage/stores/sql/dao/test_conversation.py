import unittest
from programy.storage.stores.sql.dao.conversation import Conversation
from programy.storage.stores.sql.dao.conversation import Question
from programy.storage.stores.sql.dao.conversation import Sentence
from programy.storage.stores.sql.dao.conversation import ConversationProperty
from programy.storage.stores.sql.dao.conversation import Match
from programy.storage.stores.sql.dao.conversation import MatchNode


class ConversationTests(unittest.TestCase):
    
    def test_init(self):

        conversation1 = Conversation(clientid='clientid', userid='userid', botid='botid', brainid='brainid', maxhistories=100)
        self.assertIsNotNone(conversation1)
        self.assertEqual("<Conversation(id='n/a', clientid='clientid', userid='userid', botid='botid', brainid='brainid', maxhistories='100'>", str(conversation1))
        
        conversation2 = Conversation(id=1, clientid='clientid', userid='userid', botid='botid', brainid='brainid', maxhistories=100)
        self.assertIsNotNone(conversation2)
        self.assertEqual("<Conversation(id='1', clientid='clientid', userid='userid', botid='botid', brainid='brainid', maxhistories='100'>", str(conversation2))

        question1 = Question (conversationid=1, questionno=1, srai="false")
        self.assertIsNotNone(question1)
        self.assertEqual("", str(question1))

        question2 = Question (id=1, conversationid=1, questionno=1, srai="false")
        self.assertIsNotNone(question2)
        self.assertEqual("", str(question2))

        sentence1 = Sentence (questionid=1, sentenceno=2, sentence='Hello world', response='Hi there', positivity='1.0', subjectivity='0.34')
        self.assertIsNotNone(sentence1)
        self.assertEqual("", str(sentence1))

        sentence2 = Sentence (id=1, questionid=1, sentenceno=2, sentence='Hello world', response='Hi there', positivity='1.0', subjectivity='0.34')
        self.assertIsNotNone(sentence2)
        self.assertEqual("", str(sentence2))

        convopro1 = ConversationProperty (id='%s', conversationid='%d', questionid='%d', type='%d', name='%s', value='%s')
        self.assertIsNotNone(convopro1)
        self.assertEqual("", str(convopro1))

        convopro2 = ConversationProperty (id=1, )
        self.assertIsNotNone(convopro2)
        self.assertEqual("", str(convopro2))

        match1 = Match (id='%s', max_search_depth='%d', max_search_timeout='%d', sentence='%s', response='%s', score='%s')
        self.assertIsNotNone(match1)
        self.assertEqual("", str(match1))

        match2 = Match (id=1, )
        self.assertIsNotNone(match2)
        self.assertEqual("", str(match2))

        matchnode1 = MatchNode (id='%s', matchid='%d', matchcount='%d', matchtype='%s',matchnode='%s', matchstr='%s', wildcard='%s', multiword='%s')
        self.assertIsNotNone(matchnode1)
        self.assertEqual("", str(matchnode1))

        matchnode2 = MatchNode (id=1, )
        self.assertIsNotNone(matchnode2)
        self.assertEqual("", str(matchnode2))


