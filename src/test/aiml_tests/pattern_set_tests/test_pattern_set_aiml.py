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
        self.configuration.brain_configuration._set_files = BrainFileConfiguration(files=os.path.dirname(__file__)+"/sets", extension=".txt")

class PatternsetAIMLTests(unittest.TestCase):

    def setUp(cls):
        PatternsetAIMLTests.test_client = BasicTestClient()

    def test_patten_set_match(self):
        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS AMBER")
        self.assertEqual(response, "Amber IS A NICE COLOR.")

    def test_patten_match_multi_word_set(self):
        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS AIR FORCE BLUE")
        self.assertEqual(response, "Air Force blue IS A NICE COLOR.")

    def test_patten_match_mixed_word_set(self):
        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS RED")

        self.assertEqual(response, "Red IS A NICE COLOR.")

        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS RED ORANGE")
        self.assertEqual(response, "Red Orange IS A NICE COLOR.")

        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS SACRAMENTO STATE GREEN")
        self.assertEqual(response, "Sacramento State green IS A NICE COLOR.")

    def test_patten_match_mixed_word_set_longer_sentence(self):
        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "I DO NOT LIKE RED VERY MUCH")
        self.assertEqual(response, "IT IS OK, Red IS NOT MY BEST COLOUR EITHER")

        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "I DO NOT LIKE RED ORANGE AT ALL")
        self.assertEqual(response, "IT IS OK, Red Orange IS NOT MY BEST COLOUR EITHER")

        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "I DO NOT LIKE SACRAMENTO STATE GREEN AT ALL")
        self.assertEqual(response, "IT IS OK, Sacramento State green IS NOT MY BEST COLOUR EITHER")

    def test_patten_match_mixed_word_set_at_front(self):
        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "RED IS A NICE COLOUR")
        self.assertEqual(response, "YES Red IS A LOVELY COLOUR.")

        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "RED ORANGE IS A NICE COLOUR")
        self.assertEqual(response, "YES Red Orange IS A LOVELY COLOUR.")

        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "SACRAMENTO STATE GREEN IS A NICE COLOUR")
        self.assertEqual(response, "YES Sacramento State green IS A LOVELY COLOUR.")

