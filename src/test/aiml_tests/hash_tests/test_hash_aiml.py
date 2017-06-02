import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class HashAIMLTests(unittest.TestCase):

    def setUp(cls):
        HashAIMLTests.test_client = BasicTestClient()

    def test_hash_first_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test",  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS SAY')

    def test_hash_first_no_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS')

    def test_hash_first_multi_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "WE SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS WE SAY')

    def test_hash_last_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "HELLO YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS YOU')

    def test_hash_no_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS')

    def test_hash_no_multi_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "HELLO YOU THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS YOU THERE')

    def test_hash_middle_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS HI')

    def test_hash_middle_no_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "WELL THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS')

    def test_hash_middle_multi_word(self):
        response = HashAIMLTests.test_client.bot.ask_question("test", "WELL I WAS THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS I WAS')
