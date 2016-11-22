import unittest
import logging
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/star", ".aiml", False)

class StarAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        StarAIMLTests.test_client = BasicTestClient()

    def test_star_first(self):
        response = StarAIMLTests.test_client.bot.ask_question("test",  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS SAY')

    def test_star_first_multi_words(self):
        response = StarAIMLTests.test_client.bot.ask_question("test",  "THE MAN SAYS HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS THE MAN SAYS')

    def test_star_last(self):
        response = StarAIMLTests.test_client.bot.ask_question("test",  "HELLO KEIFFBOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT')

    def test_star_last_multi_words(self):
        response = StarAIMLTests.test_client.bot.ask_question("test",  "HELLO KEIFFBOT MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT MATE')

    def test_multi_star(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL AND THERE')

    def test_multi_star_mulit_words(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "WELL THEN HI THERE MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL THEN AND THERE MATE')

    def test_star_middle(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "GOODBYE KEIFF SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF')

    def test_star_middle_mulit_words(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "GOODBYE KEIFF MATE SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF MATE')

    def test_multiple_stars_2(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "MULTIPLE STARS MATCH THIS THAT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU MATCHED FIRST AS THIS AND SECOND AS THAT')

    def test_multiple_stars_4(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "MULTI STARS ONE TWO THREE FOUR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'FOUR THREE TWO ONE')