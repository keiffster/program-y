import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

# TODO make sure topic star and that star match for set
# TODO <that><topic> can take single "1" and double "1,2" indexes

class ThatStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ThatStarTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/thatstar", ".aiml", False)

class ThatStarAIMLTests(unittest.TestCase):

    def setUp(self):
        ThatStarAIMLTests.test_client = ThatStarTestClient()

    def test_single_thatstar_word(self):
        response = ThatStarAIMLTests.test_client.bot.ask_question("test", "HELLO THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE')

        response = ThatStarAIMLTests.test_client.bot.ask_question("test", "I SAID HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HEARD YOU SAY HI THERE')
