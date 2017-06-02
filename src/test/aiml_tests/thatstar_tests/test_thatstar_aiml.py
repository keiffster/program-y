import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

# TODO make sure topic star and that star match for set
# TODO <that><topic> can take single "1" and double "1,2" indexes

class ThatStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ThatStarTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class ThatStarAIMLTests(unittest.TestCase):

    def setUp(self):
        ThatStarAIMLTests.test_client = ThatStarTestClient()

    def test_single_thatstar_word_default(self):
        # We need to ask 2 questions, first we get a response which is stored in the <that> clause, we then return it
        # on the second question

        response = ThatStarAIMLTests.test_client.bot.ask_question("test", "HELLO THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE')

        response = ThatStarAIMLTests.test_client.bot.ask_question("test", "I SAID HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HEARD YOU SAY HI THERE')
