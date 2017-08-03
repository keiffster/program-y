import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class ThatTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ThatTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files=os.path.dirname(__file__)


class ThatAIMLTests(unittest.TestCase):

    def setUp(self):
        ThatAIMLTests.test_client = ThatTestClient()

    def test_that_single_that_word(self):
        response = ThatAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE')

        response = ThatAIMLTests.test_client.bot.ask_question("test", "HELLO AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO WITH THAT')

    def test_coffee_yes_question(self):
        response = ThatAIMLTests.test_client.bot.ask_question("test", "I LIKE COFFEE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DO YOU TAKE CREAM OR SUGAR IN YOUR COFFEE?')

        response = ThatAIMLTests.test_client.bot.ask_question("test", "YES")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'I DO TOO.')

    def test_coffee_no_question(self):
        response = ThatAIMLTests.test_client.bot.ask_question("test", "I LIKE COFFEE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DO YOU TAKE CREAM OR SUGAR IN YOUR COFFEE?')

        response = ThatAIMLTests.test_client.bot.ask_question("test", "NO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'REALLY? I HAVE A HARD TIME DRINKING BLACK COFFEE.')

    def test_that_case(self):
        response = ThatAIMLTests.test_client.bot.ask_question("test", "CASE HELLO1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'CASE HI THERE')

        response = ThatAIMLTests.test_client.bot.ask_question("test", "CASE HELLO AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'CASE HELLO RESPONSE')

        response = ThatAIMLTests.test_client.bot.ask_question("test", "CASE HELLO2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Case Hi There')

        response = ThatAIMLTests.test_client.bot.ask_question("test", "CASE HELLO AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'CASE HELLO RESPONSE')

    def test_multiple_sentenes(self):
        response = ThatAIMLTests.test_client.bot.ask_question("test", "START")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'This is sentence 1. This is sentence two.')

        response = ThatAIMLTests.test_client.bot.ask_question("test", "CONTINUE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'TEST PASS')
