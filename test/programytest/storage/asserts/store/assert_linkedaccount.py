import unittest

class LinkedAccountStoreAsserts(unittest.TestCase):

    def assert_linkedaccounts_storage(self, store):
        store.empty()

        store.link_accounts(1, 2)
        store.link_accounts(1, 3)
        store.commit()

        accounts = store.linked_accounts(1)
        self.assertIsNotNone(accounts)
        self.assertEqual(2, len(accounts))
        self.assertTrue(2 in accounts)
        self.assertTrue(3 in accounts)

        accounts = store.primary_account(2)
        self.assertIsNotNone(accounts)
        self.assertEqual(1, len(accounts))
        self.assertTrue(1 in accounts)

        accounts = store.primary_account(3)
        self.assertIsNotNone(accounts)
        self.assertEqual(1, len(accounts))
        self.assertTrue(1 in accounts)

        store.unlink_account(1, 2)
        store.commit()
        accounts = store.linked_accounts(1)
        self.assertIsNotNone(accounts)
        self.assertEqual(1, len(accounts))
        self.assertTrue(3 in accounts)

        store.unlink_accounts(1)
        store.commit()
        store.commit()
        accounts = store.linked_accounts(1)
        self.assertIsNotNone(accounts)
        self.assertEqual(0, len(accounts))

