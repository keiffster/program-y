import unittest
import os

from programytest.client import TestClient


class BankBalanceTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(BankBalanceTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class BankBalanceAIMLTests(unittest.TestCase):

    def setUp (self):
        client = BankBalanceTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_balance(self):
        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS MY BANK BALANCE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Your bank balance is currently £0.00.')
