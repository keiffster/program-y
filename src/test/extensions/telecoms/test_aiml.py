import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration


class TelecomsMinutesTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(TelecomsMinutesTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class TelecomsMinutesAIMLTests(unittest.TestCase):

    def setUp (self):
        TelecomsMinutesAIMLTests.test_client = TelecomsMinutesTestsClient()

    def test_balance(self):
        response = TelecomsMinutesAIMLTests.test_client.bot.ask_question("testif", "HOW MANY MINUTES DO I HAVE LEFT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'This month you have 0 minutes available and have consumed 0 minutes.')

