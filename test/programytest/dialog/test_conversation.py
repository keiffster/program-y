import unittest

from programy.dialog.dialog import Question, Conversation
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class ConversationTests(unittest.TestCase):

    def test_conversation(self):

        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual(0, len(conversation._questions))
        self.assertEqual(3, conversation._max_histories)
        self.assertEqual(1, len(conversation._properties))

        with self.assertRaises(Exception):
            conversation.current_question()
        with self.assertRaises(Exception):
            conversation.previous_nth_question(0)

        question1 = Question.create_from_text(client_context, "Hello There")
        conversation.record_dialog(question1)
        self.assertEqual(question1, conversation.current_question())
        with self.assertRaises(Exception):
            conversation.previous_nth_question(1)

        question2 = Question.create_from_text(client_context, "Hello There Again")
        conversation.record_dialog(question2)
        self.assertEqual(question2, conversation.current_question())
        self.assertEqual(question1, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(3)

        question3 = Question.create_from_text(client_context, "Hello There Again Again")
        conversation.record_dialog(question3)
        self.assertEqual(question3, conversation.current_question())
        self.assertEqual(question2, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(4)

        # Max Histories for this test is 3
        # Therefore we should see the first question, pop of the stack

        question4 = Question.create_from_text(client_context, "Hello There Again Again Again")
        conversation.record_dialog(question4)
        self.assertEqual(question4, conversation.current_question())
        self.assertEqual(question3, conversation.previous_nth_question(1))
        with self.assertRaises(Exception):
            conversation.previous_nth_question(5)

    def test_parse_last_sentences_from_response(self):

        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        conversation = Conversation(client_context)
        self.assertIsNotNone(conversation)

        response = "Hello World"
        that = conversation.parse_last_sentences_from_response(response)
        self.assertEqual("Hello World", that)

        response = "Hello World. Second sentence"
        that = conversation.parse_last_sentences_from_response(response)
        self.assertEqual("Second sentence", that)

        response = "Hello World. Second sentence. Third Sentence"
        that = conversation.parse_last_sentences_from_response(response)
        self.assertEqual("Third Sentence", that)