import unittest

from programy.storage.stores.nosql.mongo.dao.conversation import Conversation

from programy.dialog.question import Question
from programy.dialog.conversation import Conversation as Convo

from programytest.client import TestClient

class ConversationTests(unittest.TestCase):

    def test_init_blank(self):
        conversation1 = Conversation(None, None)
        self.assertIsNotNone(conversation1)
        self.assertIsNone(conversation1.clientid)
        self.assertIsNone(conversation1.userid)
        self.assertIsNone(conversation1.botid)
        self.assertIsNone(conversation1.brainid)
        self.assertIsNone(conversation1.conversation)

    def test_init_context_and_converstion(self):

        client = TestClient()
        client_context = client.create_client_context("testuser")

        convo = Convo(client_context)

        question = Question.create_from_text(client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        convo.record_dialog(question)

        conversation = Conversation(client_context, convo)
        self.assertIsNotNone(conversation)

        self.assertEqual(client_context.client.id, conversation.clientid)
        self.assertEqual(client_context.userid, conversation.userid)
        self.assertEqual(client_context.bot.id, conversation.botid)
        self.assertEqual(client_context.brain.id, conversation.brainid)
        self.assertIsNotNone(conversation.conversation)

        doc = conversation.to_document()
        self.assertEqual({'clientid': 'testclient', 'userid': 'testuser', 'botid': 'bot', 'brainid': 'brain', 'conversation': {'client_context': {'clientid': 'testclient', 'userid': 'testuser', 'botid': 'bot', 'brainid': 'brain', 'depth': 0}, 'questions': [{'srai': False, 'sentences': [{'words': ['Hello', 'world'], 'response': 'Hello matey', 'positivity': 0.0, 'subjectivity': 0.5}], 'current_sentence_no': -1, 'properties': {}}], 'max_histories': 100, 'properties': {'topic': '*'}}},
                          doc)

        conversation2 = Conversation.from_document(client_context, doc)
        self.assertIsNotNone(conversation2)
        self.assertEqual(conversation2.clientid, conversation.clientid)
        self.assertEqual(conversation2.userid, conversation.userid)
        self.assertEqual(conversation2.botid, conversation.botid)
        self.assertEqual(conversation2.brainid, conversation.brainid)
