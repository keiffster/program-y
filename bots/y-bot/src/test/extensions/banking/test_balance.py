import unittest

from extensions.banking.balance import BankingBalanceExtension

class BankBalanceExtensionTests(unittest.TestCase):

    def test_balance(self):

        balance = BankingBalanceExtension()
        self.assertIsNotNone(balance)

        result = balance.execute("NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0.00", result)