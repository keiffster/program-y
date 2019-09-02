import unittest

from programy.dialog.question import Question
from programy.dialog.conversation import Conversation

from programytest.client import TestClient


class ConverstionStoreAsserts(unittest.TestCase):

    def assert_conversation_storage(self, store, can_empty=True, test_load=True):

        if can_empty is True:
            store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.store_conversation(client_context, conversation)

        store.commit()

        if test_load is True:
            conversation2 = Conversation(client_context)
            store.load_conversation(client_context, conversation2)

            self.assertEqual(1, len(conversation2.questions))
            self.assertEqual(1, len(conversation2.questions[0].sentences))
            self.assertEqual("Hello There", conversation2.questions[0].sentences[0].text(client_context))
            self.assertEqual("Hi", conversation2.questions[0].sentences[0].response)

        if can_empty is True:
            store.empty()
