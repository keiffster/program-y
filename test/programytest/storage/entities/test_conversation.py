import unittest

from programy.storage.entities.conversation import ConversationStore
from programy.dialog.question import Question
from programy.dialog.conversation import Conversation

from programytest.client import TestClient

class ConversationStoreTests(unittest.TestCase):

    def test_store_conversation(self):
        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        convo_store = ConversationStore()
        with self.assertRaises(NotImplementedError):
            convo_store.store_conversation(client_context, conversation)
