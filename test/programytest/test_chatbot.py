import unittest

from programy.chatbot import ProgramYChatbot

from programytest.clients.arguments import MockArgumentParser

class ChatBotTests(unittest.TestCase):

    def test_init(self):

        arguments = MockArgumentParser()
        chatbot = ProgramYChatbot(arguments)
        chatbot.add_local_properties()
        self.assertIsNotNone(chatbot)

        client_context = chatbot.create_client_context("console")
        self.assertIsNotNone(client_context)
        self.assertIsNotNone(client_context.brain)

        self.assertEqual(client_context.brain.properties.property("name"), "ProgramY")
        self.assertEqual(client_context.brain.properties.property("app_version"), "1.0.0")
        self.assertEqual(client_context.brain.properties.property("grammar_version"), "1.0.0")
        self.assertIsNotNone(client_context.brain.properties.property("birthdate"))
