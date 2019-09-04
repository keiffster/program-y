import unittest

from programy.services.openchatbot.collection import OpenChatBotCollection
from programy.config.brain.openchatbots import BrainOpenChatBotsConfiguration
from programy.config.brain.openchatbot import BrainOpenChatBotConfiguration


class OpenChatBotCollectionTests(unittest.TestCase):

    def test_load_from_configuration(self):

        config = BrainOpenChatBotsConfiguration()
        chatbot1_config = BrainOpenChatBotConfiguration('chatbot1')
        chatbot1_config._url = "http://localhost:5959/api/rest/v2.0/ask"
        chatbot1_config._method = ["GET"]
        config._openchatbots["chatbot1"] = chatbot1_config

        collection = OpenChatBotCollection()
        collection.load_from_configuration(config)

        self.assertTrue(collection.exists("chatbot1"))
        chatbot = collection.openchatbot("chatbot1")
        self.assertIsNotNone(chatbot)
        self.assertEqual(chatbot.name, "chatbot1")
        self.assertEqual(chatbot.url, "http://localhost:5959/api/rest/v2.0/ask")
        self.assertEqual(chatbot.methods, ["GET"])
