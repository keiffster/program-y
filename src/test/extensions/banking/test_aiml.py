import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration


class BankBalanceTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(BankBalanceTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class BankBalanceAIMLTests(unittest.TestCase):

    def setUp (self):
        BankBalanceAIMLTests.test_client = BankBalanceTestsClient()

    def test_balance(self):
        response = BankBalanceAIMLTests.test_client.bot.ask_question("testif", "WHAT IS MY BANK BALANCE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Your bank balance is currently £0.00.')

