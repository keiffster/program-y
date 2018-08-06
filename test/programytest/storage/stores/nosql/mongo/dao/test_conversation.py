import unittest

from programy.storage.stores.nosql.mongo.dao.conversation import Conversation

from programy.dialog.dialog import Question
from programy.dialog.dialog import Conversation as Convo

from programytest.client import TestClient

class ConversationTests(unittest.TestCase):

    def test_init_blank(self):
        conversation = Conversation(None, None)
        self.assertIsNotNone(conversation)
        self.assertIsNone(conversation.clientid)
        self.assertIsNone(conversation.userid)
        self.assertIsNone(conversation.botid)
        self.assertIsNone(conversation.brainid)
        self.assertIsNone(conversation.conversation)

    def test_init_context_and_converstion(self):

        client = TestClient()
        client_context = client.create_client_context("tesuser")

        convo = Convo(client_context)

        question = Question.create_from_text(client_context.brain.tokenizer, "Hello world")
        question.current_sentence()._response = "Hello matey"
        convo.record_dialog(question)

        conversation = Conversation(client_context, convo)
        self.assertIsNotNone(conversation)

        self.assertEquals(client_context.client.id, conversation.clientid)
        self.assertEquals(client_context.userid, conversation.userid)
        self.assertEquals(client_context.bot.id, conversation.botid)
        self.assertEquals(client_context.brain.id, conversation.brainid)
        self.assertIsNotNone(conversation.conversation)