import unittest
import os

from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class OrderingTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(OrderingTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class OrderingAIMLTests(unittest.TestCase):

    def setUp(self):
        OrderingAIMLTests.test_client = OrderingTestClient()
        OrderingAIMLTests.test_client.bot.brain.sets._sets["COLOR"] = {"RED": [["RED"]]}
        OrderingAIMLTests.test_client.bot.brain.sets._sets["ANIMAL"] = {"DOLPHIN": [["DOLPHIN"]]}

    def test_basic_no_match(self):
        response = OrderingAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS BLUE")
        self.assertEqual(response, "i didn't recognize BLUE AS A COLOR.")

    def test_basic_match(self):
        response = OrderingAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS RED")
        self.assertEqual(response, "Red IS A NICE COLOR.")

    def test_basic_exact_match(self):
        response = OrderingAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS GREEN")
        self.assertEqual(response, "Green IS MY FAVORITE COLOR TOO!")

    def test_hash_v_star(self):
        OrderingAIMLTests.test_client.bot.brain.dump_tree()
        response = OrderingAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE ANIMAL IS A DOLPHIN")
        self.assertEqual(response, "HASH SELECTED")

        OrderingAIMLTests.test_client.bot.brain.dump_tree()
        response = OrderingAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE ANIMAL IS AN AARDVARK")
        self.assertEqual(response, "SELECTED ONCE")
