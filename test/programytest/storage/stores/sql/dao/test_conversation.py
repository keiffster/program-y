import unittest

from programy.storage.stores.sql.dao.conversation import Conversation
from programy.storage.stores.sql.dao.conversation import ConversationProperty
from programy.storage.stores.sql.dao.conversation import Match
from programy.storage.stores.sql.dao.conversation import MatchNode
from programy.storage.stores.sql.dao.conversation import Question
from programy.storage.stores.sql.dao.conversation import Sentence


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
        self.assertEqual("<Question(id='n/a', conversationid='1', questionno='1', srai='false'>", str(question1))

        question2 = Question (id=1, conversationid=1, questionno=1, srai="false")
        self.assertIsNotNone(question2)
        self.assertEqual("<Question(id='1', conversationid='1', questionno='1', srai='false'>", str(question2))

        sentence1 = Sentence (questionid=1, sentenceno=2, sentence='Hello world', response='Hi there', positivity='1.0', subjectivity='0.34')
        self.assertIsNotNone(sentence1)
        self.assertEqual("<Sentence(id='n/a', questionid='1', sentenceno='2', sentence='Hello world', response='Hi there', positivity='1.0', subjectivity='0.34'>", str(sentence1))

        sentence2 = Sentence (id=1, questionid=1, sentenceno=2, sentence='Hello world', response='Hi there', positivity='1.0', subjectivity='0.34')
        self.assertIsNotNone(sentence2)
        self.assertEqual("<Sentence(id='1', questionid='1', sentenceno='2', sentence='Hello world', response='Hi there', positivity='1.0', subjectivity='0.34'>", str(sentence2))

        convopro1 = ConversationProperty (conversationid=1, questionid=2, type=3, name='name', value='value')
        self.assertIsNotNone(convopro1)
        self.assertEqual("<ConversationProperty(id='n/a', conversationid='1', questionid='2', type='3', name='name', value='value')>", str(convopro1))

        convopro2 = ConversationProperty (id=1, conversationid=1, questionid=2, type=3, name='name', value='value')
        self.assertIsNotNone(convopro2)
        self.assertEqual("<ConversationProperty(id='1', conversationid='1', questionid='2', type='3', name='name', value='value')>", str(convopro2))

        match1 = Match (max_search_depth=100, max_search_timeout=100, sentence='HELLO WORLD', response='Hi there', score='0.99')
        self.assertIsNotNone(match1)
        self.assertEqual("<Match(id='n/a', max_search_depth='100', max_search_timeout='100', sentence='HELLO WORLD', response='Hi there', score='0.99')>", str(match1))

        match2 = Match (id=1, max_search_depth=100, max_search_timeout=100, sentence='HELLO WORLD', response='Hi there', score='0.99')
        self.assertIsNotNone(match2)
        self.assertEqual("<Match(id='1', max_search_depth='100', max_search_timeout='100', sentence='HELLO WORLD', response='Hi there', score='0.99')>", str(match2))

        matchnode1 = MatchNode (matchid=1, matchcount=2, matchtype='WORD', matchnode='NODE', matchstr='HELLO', wildcard='*', multiword='False')
        self.assertIsNotNone(matchnode1)
        self.assertEqual("<MatchNode(id='n/a', matchid='1', matchcount='2', matchtype='WORD', matchnode='NODE', matchstr='HELLO', wildcard='*', multiword='False')>", str(matchnode1))

        matchnode2 = MatchNode (id=1, matchid=1, matchcount=2, matchtype='WORD', matchnode='NODE', matchstr='HELLO', wildcard='*', multiword='False')
        self.assertIsNotNone(matchnode2)
        self.assertEqual("<MatchNode(id='1', matchid='1', matchcount='2', matchtype='WORD', matchnode='NODE', matchstr='HELLO', wildcard='*', multiword='False')>", str(matchnode2))


