import unittest

from programy.extensions.banking.balance import BankingBalanceExtension

class BankBalanceExtensionTests(unittest.TestCase):

    def setUp(self):
        self.bot = None
        self.clientid = "testid"

    def test_balance(self):

        balance = BankingBalanceExtension()
        self.assertIsNotNone(balance)

        result = balance.execute(self.bot, self.clientid, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 00 CREDIT", result)