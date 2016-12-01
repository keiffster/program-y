import unittest
import os

from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/basics", ".aiml", False)

class BasicAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BasicAIMLTests.test_client = BasicTestClient()

    def test_basic_no_response(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test",  "NO RESPONSE")
        self.assertEqual(response, '')

    def test_basic_one_word(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test",  "HELLO")
        self.assertEqual(response, "HELLO, WORLD")

    def test_basic_two_words(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test",  "HELLO THERE")
        self.assertEqual(response, "HOW ARE YOU")

    def test_basic_three_words(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test",  "HELLO THERE NOW")
        self.assertEqual(response, "HOW ARE YOU NOW")

    def test_basic_no_match(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "HELLO YOU")
        self.assertEqual(response, '')

    def test_star_after(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test",  "HI")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "HI THERE")
        self.assertEqual(response, "HI, HOW ARE YOU")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "HI THERE MATE")
        self.assertEqual(response, "HI, HOW ARE YOU")

    def test_star_before(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "HEY")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL HEY")
        self.assertEqual(response, "HEY, HOW ARE YOU")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL NOW HEY")
        self.assertEqual(response, "HEY, HOW ARE YOU")

    def test_star_before2(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "HELLO THERE HEY")
        self.assertEqual(response, "HEY, HOW ARE YOU")

    def test_hash_after(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "HOWDY")
        self.assertEqual(response, "HOWDY PARTNER")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "HOWDY MATE")
        self.assertEqual(response, "HOWDY PARTNER")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "HOWDY THERE MATE")
        self.assertEqual(response, "HOWDY PARTNER")

    def test_hash_before(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "YO")
        self.assertEqual(response, "YO, HOW ARE YOU")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "HEY YO")
        self.assertEqual(response, "YO, HOW ARE YOU")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "HEY NOW YO")
        self.assertEqual(response, "YO, HOW ARE YOU")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "HELLO THERE YO")
        self.assertEqual(response, "YO, HOW ARE YOU")

    def test_star_star(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "GOODBYE")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "GOODBYE MATE")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL GOODBYE MATE")
        self.assertEqual(response, "BYE BYE")

    def test_star_hash(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "SEEYA")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "SEEYA MATE")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL SEEYA")
        self.assertEqual(response, "BYE THE NOW")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL SEEYA MATE")
        self.assertEqual(response, "BYE THE NOW")

    def test_hash_hash(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "LATER")
        self.assertEqual(response, "LATERZ")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "LATER MATE")
        self.assertEqual(response, "LATERZ")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL LATER")
        self.assertEqual(response, "LATERZ")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL LATER MATE")
        self.assertEqual(response, "LATERZ")

    def test_hash_star(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "FAREWELL")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL FAREWELL")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "WELL FAREWELL MATE")
        self.assertEqual(response, "UNTIL TOMORROW")

        response = BasicAIMLTests.test_client.bot.ask_question("test", "FAREWELL MATE")
        self.assertEqual(response, "UNTIL TOMORROW")

    def test_hash_middle(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "MORNING MATE")
        self.assertEqual(response, 'GOOD MORNING')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "MORNING THERE MATE")
        self.assertEqual(response, 'GOOD MORNING')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "MORNING MY GOOD MATE")
        self.assertEqual(response, 'GOOD MORNING')

    def test_hash_middle_with_extra(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "MORNING MATE AHOY")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "MORNING MY MATE AHOY")
        self.assertEqual(response, '')

    def test_star_middle(self):
        response = BasicAIMLTests.test_client.bot.ask_question("test", "EVENING CHUM")
        self.assertEqual(response, '')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "EVENING THERE CHUM")
        self.assertEqual(response, 'GOOD EVENING')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "EVENING THERE MY CHUM")
        self.assertEqual(response, 'GOOD EVENING')

        response = BasicAIMLTests.test_client.bot.ask_question("test", "EVENING THERE CHUM HALLO")
        self.assertEqual(response, '')
