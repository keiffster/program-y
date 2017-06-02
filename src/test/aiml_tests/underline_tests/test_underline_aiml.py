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

class UnderlineAIMLTests(unittest.TestCase):

    def setUp(cls):
        UnderlineAIMLTests.test_client = BasicTestClient()

    def test_underline_first(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test",  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS SAY')

    def test_underline_first_multi_words(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test",  "THE MAN SAYS HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS THE MAN SAYS')

    def test_underline_last(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test",  "HELLO KEIFFBOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT')

    def test_underline_last_multi_words(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test",  "HELLO KEIFFBOT MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT MATE')

    def test_multi_underline(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test", "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL AND THERE')

    def test_multi_underline_mulit_words(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test", "WELL THEN HI THERE MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL THEN AND THERE MATE')

    def test_underline_middle(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test", "GOODBYE KEIFF SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF')

    def test_underline_middle_mulit_words(self):
        response = UnderlineAIMLTests.test_client.bot.ask_question("test", "GOODBYE KEIFF MATE SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF MATE')