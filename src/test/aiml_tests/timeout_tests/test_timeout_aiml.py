import unittest
import os
from test.aiml_tests.client import TestClient

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)

class TimeoutAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TimeoutAIMLTests.test_client = BasicTestClient()

    def test_max_question_recursion_timeout(self):

        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_question_recursion = 10
        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_question_timeout = -1
        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_search_depth = -1
        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_search_timeout = -1

        response = TimeoutAIMLTests.test_client.bot.ask_question("test",  "START")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')

    def test_max_question_timeout_timeout(self):

        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_question_recursion = -1
        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_question_timeout = 0.1
        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_search_depth = -1
        TimeoutAIMLTests.test_client.configuration.bot_configuration._max_search_timeout = -1

        response = TimeoutAIMLTests.test_client.bot.ask_question("test",  "START")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')
