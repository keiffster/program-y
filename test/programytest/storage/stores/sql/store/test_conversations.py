import unittest

from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts

from programy.storage.stores.sql.store.conversations import SQLConversationStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.dao.conversation import ConversationProperty as ConversationPropertyDAO

import programytest.storage.engines as Engines
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match
from programy.dialog.question import Question
from programy.dialog.conversation import Conversation
from programy.parser.pattern.nodes.word import PatternWordNode

from programytest.client import TestClient


class SQLConversationStoreTests(ConverstionStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_read_write_conversation_properties_in_db(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        client = TestClient()
        client_context = client.create_client_context("user1")

        store.empty()

        properties1 = {"key1": "value1", "key2": "value2"}

        store._write_properties_to_db(client_context, 1, 2, ConversationPropertyDAO.CONVERSATION, properties1)

        store.commit()

        properties2 = {}

        store._read_properties_from_db(client_context, 1, 2, ConversationPropertyDAO.CONVERSATION, properties2)

        self.assertEquals({"key1": "value1", "key2": "value2"}, properties2)

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_read_write_question_properties_in_db(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        client = TestClient()
        client_context = client.create_client_context("user1")

        store.empty()

        properties1 = {"key1": "value1", "key2": "value2"}

        store._write_properties_to_db(client_context, 1, 2, ConversationPropertyDAO.QUESTION, properties1)

        store.commit()

        properties2 = {}

        store._read_properties_from_db(client_context, 1, 2, ConversationPropertyDAO.QUESTION, properties2)

        self.assertEquals({"key1": "value1", "key2": "value2"}, properties2)

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_read_write_matches_in_db(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        matched_context1 = MatchContext(100, 100, sentence="Hello", response="Hi There")
        matched_context1.matched_nodes.append(Match(Match.WORD, PatternWordNode("Hello"), "Hello"))

        store._write_matches_to_db(client_context, matched_context1, 1)

        store.commit()

        matched_context2 = MatchContext(0, 0)

        store._read_matches_from_db(client_context, matched_context2, 1)

        self.assertEquals(1, len(matched_context2.matched_nodes))
        self.assertEquals(Match.WORD, matched_context2.matched_nodes[0].matched_node_type)
        self.assertEquals("WORD [Hello]", matched_context2.matched_nodes[0].matched_node_str)
        self.assertFalse(matched_context2.matched_nodes[0].matched_node_multi_word)
        self.assertFalse(matched_context2.matched_nodes[0].matched_node_wildcard)
        self.assertEquals(1, len(matched_context2.matched_nodes[0].matched_node_words))
        self.assertEquals(["Hello"], matched_context2.matched_nodes[0].matched_node_words)

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_match_context_in_db(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        matched_context1 = MatchContext(100, 100, sentence="Hello", response="Hi There")
        matched_context1._matched_nodes = []
        matched_context1._template_node = None

        store._write_match_context_to_db(client_context, 1, matched_context1)

        store.commit()

        matched_context2 = MatchContext(100, 100)

        store._read_match_context_from_db(client_context, 1, matched_context2)

        self.assertEquals(100, matched_context2.max_search_timeout)
        self.assertEquals(100, matched_context2.max_search_depth)
        self.assertEquals("Hello", matched_context2.sentence)
        self.assertEquals("Hi There", matched_context2.response)

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_sentences_in_db(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        question1.sentence(0)._positivity = 0.5
        question1.sentence(0)._subjectivity = 0.6

        store._write_sentences_to_db(client_context, 1, question1)

        store.commit()

        question2 = Question()

        store._read_sentences_from_db(client_context, 1, question2)

        self.assertEquals(1, len(question2.sentences))
        self.assertEquals(0.5, question2.sentences[0].positivity)
        self.assertEquals(0.6, question2.sentences[0].subjectivity)
        self.assertEquals(["Hello", "There"], question2.sentences[0].words)
        self.assertEquals("Hi", question2.sentences[0].response)

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_questions_in_db(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation1 = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        question1.sentence(0)._positivity = 0.5
        question1.sentence(0)._subjectivity = 0.6
        conversation1.record_dialog(question1)

        store._write_questions_to_db(client_context, 1, conversation1)
        store.commit()

        conversation2 = Conversation(client_context)

        store._read_questions_from_db(client_context, 1, conversation2)

        self.assertEquals(1, len(conversation2.questions))

        self.assertEquals(1, len(conversation2.questions[0].sentences))
        self.assertEquals(0.5, conversation2.questions[0].sentences[0].positivity)
        self.assertEquals(0.6, conversation2.questions[0].sentences[0].subjectivity)
        self.assertEquals(["Hello", "There"], conversation2.questions[0].sentences[0].words)
        self.assertEquals("Hi", conversation2.questions[0].sentences[0].response)

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_conversation_in_db(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation1 = Conversation(client_context)

        conversation1.properties['ckey1'] = "cvalue1"
        conversation1.properties['ckey2'] ="cvalue2"

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        question1.sentence(0)._positivity = 0.5
        question1.sentence(0)._subjectivity = 0.6
        question1.properties['qkey1'] = "qvalue1"
        question1.properties['qkey2'] = "qvalue2"

        conversation1.record_dialog(question1)

        store.store_conversation(client_context, conversation1)

        store.commit ()

        conversation2 = Conversation(client_context)

        store.load_conversation (client_context, conversation2)

        self.assertEquals(conversation2.properties['ckey1'], "cvalue1")
        self.assertEquals(conversation2.properties['ckey2'], "cvalue2")

        self.assertEquals(conversation2.questions[0].sentence(0).response, "Hi")
        self.assertEquals(conversation2.questions[0].sentence(0)._positivity, 0.5)
        self.assertEquals(conversation2.questions[0].sentence(0)._subjectivity, 0.6)

        self.assertEquals(conversation2.questions[0].properties['qkey1'], "qvalue1")
        self.assertEquals(conversation2.questions[0].properties['qkey2'], "qvalue2")

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_conversation_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_conversation_storage(store)
