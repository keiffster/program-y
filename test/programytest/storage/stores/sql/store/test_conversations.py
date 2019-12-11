import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.conversations import SQLConversationStore
from programytest.client import TestClient
from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts
from programy.storage.stores.sql.dao.conversation import Conversation as ConversationDAO
from programy.storage.stores.sql.dao.conversation import Question as QuestionDAO
from programy.storage.stores.sql.dao.conversation import Sentence as SentenceDAO
from programy.storage.stores.sql.dao.conversation import ConversationProperty as ConversationPropertyDAO
from programy.storage.stores.sql.dao.conversation import Match as MatchDAO
from programy.storage.stores.sql.dao.conversation import MatchNode as MatchNodeDAO


class SQLConversationStoreTests(ConverstionStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_get_all(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)

        with self.assertRaises(Exception):
            store._get_all()

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

        self.assertEqual({"key1": "value1", "key2": "value2"}, properties2)

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

        self.assertEqual({"key1": "value1", "key2": "value2"}, properties2)

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

        self.assertEqual(1, len(matched_context2.matched_nodes))
        self.assertEqual(Match.WORD, matched_context2.matched_nodes[0].matched_node_type)
        self.assertEqual("WORD [Hello]", matched_context2.matched_nodes[0].matched_node_str)
        self.assertFalse(matched_context2.matched_nodes[0].matched_node_multi_word)
        self.assertFalse(matched_context2.matched_nodes[0].matched_node_wildcard)
        self.assertEqual(1, len(matched_context2.matched_nodes[0].matched_node_words))
        self.assertEqual(["Hello"], matched_context2.matched_nodes[0].matched_node_words)

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

        self.assertEqual(100, matched_context2.max_search_timeout)
        self.assertEqual(100, matched_context2.max_search_depth)
        self.assertEqual("Hello", matched_context2.sentence)
        self.assertEqual("Hi There", matched_context2.response)

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

        self.assertEqual(1, len(question2.sentences))
        self.assertEqual(0.5, question2.sentences[0].positivity)
        self.assertEqual(0.6, question2.sentences[0].subjectivity)
        self.assertEqual(["Hello", "There"], question2.sentences[0].words)
        self.assertEqual("Hi", question2.sentences[0].response)

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

        self.assertEqual(1, len(conversation2.questions))

        self.assertEqual(1, len(conversation2.questions[0].sentences))
        self.assertEqual(0.5, conversation2.questions[0].sentences[0].positivity)
        self.assertEqual(0.6, conversation2.questions[0].sentences[0].subjectivity)
        self.assertEqual(["Hello", "There"], conversation2.questions[0].sentences[0].words)
        self.assertEqual("Hi", conversation2.questions[0].sentences[0].response)

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

        self.assertEqual(conversation2.properties['ckey1'], "cvalue1")
        self.assertEqual(conversation2.properties['ckey2'], "cvalue2")

        self.assertEqual(conversation2.questions[0].sentence(0).response, "Hi")
        self.assertEqual(conversation2.questions[0].sentence(0)._positivity, 0.5)
        self.assertEqual(conversation2.questions[0].sentence(0)._subjectivity, 0.6)

        self.assertEqual(conversation2.questions[0].properties['qkey1'], "qvalue1")
        self.assertEqual(conversation2.questions[0].properties['qkey2'], "qvalue2")

        store.empty()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_conversation_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_conversation_storage(store)

    def patch_get_conversation_dao(self, client_context):
        return ConversationDAO(id=1,
                               clientid="client1",
                               userid="user1",
                               botid="bot1",
                               brainid="brain1",
                               maxhistories=100)

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_conversation_dao", patch_get_conversation_dao)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_existing_conversation(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_conversation_dao2(self, client_context):
        return None

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_conversation_dao", patch_get_conversation_dao2)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_no_conversation(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_question_dao(self, conversationid, question_no):
        return QuestionDAO(id=1,
                           conversationid=conversationid,
                           questionno=question_no,
                           srai=False)

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_question_dao", patch_get_question_dao)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_existing_question(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_question_dao2(self, conversationid, question_no):
        return None

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_question_dao", patch_get_question_dao2)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_noquestion(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_sentence_dao(self, questionid, sentence_no):
        return SentenceDAO(id=1,
                           questionid = questionid,
                           sentenceno = sentence_no,
                           sentence = "Hello",
                           response = "Hi There",
                           positivity = "0.5",
                           subjectivity = "0.5")

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_sentence_dao", patch_get_sentence_dao)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_existing_sentence(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_sentence_dao2(self, questionid, sentence_no):
        return None

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_sentence_dao", patch_get_sentence_dao2)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_no_sentence(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_match_dao(self, sentenceid):
        return MatchDAO(id=1,
                        sentenceid = sentenceid,
                        max_search_depth = 99,
                        max_search_timeout = 99,
                        sentence = "Hello",
                        response = "Hi there",
                        score = "1.0")

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_match_dao", patch_get_match_dao)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_existing_match(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_match_dao2(self, sentenceid):
        return None

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_match_dao", patch_get_match_dao2)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_no_match(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_matchnode_dao(self, matchid, match_count):
        return MatchNodeDAO(id = 1,
                            matchid = matchid,
                            matchcount = match_count,
                            matchtype = "WORD",
                            matchnode = "WORD",
                            matchstr = "HELLO",
                            wildcard = False,
                            multiword = False)

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_matchnode_dao", patch_get_matchnode_dao)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_existing_matchnode(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_matchnode_dao2(self, matchid, match_count):
        return None

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_matchnode_dao", patch_get_matchnode_dao2)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_no_matchnode(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_property_dao(self, conversationid, questionid, proptype, name):
        return ConversationPropertyDAO(id=1,
                                       conversationid = conversationid,
                                       questionid =questionid,
                                       type = proptype,
                                       name = name,
                                       value = "value")

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_property_dao", patch_get_property_dao)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_existing_property_unmatched(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_property_dao2(self, conversationid, questionid, proptype, name):
        return ConversationPropertyDAO(id=1,
                                       conversationid = conversationid,
                                       questionid =questionid,
                                       type = proptype,
                                       name = "topic",
                                       value = "*")

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_property_dao", patch_get_property_dao2)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_existing_property_matched(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)

    def patch_get_property_dao3(self, conversationid, questionid, proptype, name):
        return None

    @patch("programy.storage.stores.sql.store.conversations.SQLConversationStore._get_property_dao", patch_get_property_dao3)
    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_storage_where_no_property(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_just_conversation_storage(store)
