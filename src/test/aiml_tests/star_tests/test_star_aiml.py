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

    def test_star_with_set(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "STAR WITH SET 666")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SET IS 666')

    def test_multi_stars_with_set(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "STAR WITH SETS 666 999")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SETS ARE 666 AND 999')

    def test_mixed_stars_and_sets(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "MIXED STARS AND SETS 11 22 33 44 55")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STARS ARE 11 AND 22 AND 33 AND 44 AND 55')

    def test_recursion_one_star(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "RECURSIVE TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ENDED')

    def test_recursion_two_stars(self):
        response = StarAIMLTests.test_client.bot.ask_question("test", "RECURSIVE TEST THIS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'RECURSED ENDED')

    def test_recursion_four_stars(self):
        StarAIMLTests.test_client.dump_bot_brain_tree()
        response = StarAIMLTests.test_client.bot.ask_question("test", "RECURSIVE TEST THIS THAT OTHER")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'RECURSED RECURSED RECURSED ENDED')