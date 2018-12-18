import unittest

class LinkedAccountStoreAsserts(unittest.TestCase):

    def assert_linkedaccounts_storage(self, store):

        store.empty()

        store.link_accounts("user1", "user2")
        store.link_accounts("user1", "user3")
        store.commit()

        accounts = store.linked_accounts("user1")
        self.assertIsNotNone(accounts)
        self.assertEqual(2, len(accounts))
        self.assertTrue("user2" in accounts)
        self.assertTrue("user3" in accounts)

        accounts = store.primary_account("user2")
        self.assertIsNotNone(accounts)
        self.assertTrue("user1" in accounts)

        accounts = store.primary_account("user3")
        self.assertIsNotNone(accounts)
        self.assertTrue("user1" in accounts)

        store.unlink_accounts("user1")
        store.commit()
        accounts = store.linked_accounts("user1")
        self.assertIsNotNone(accounts)
        self.assertEqual(0, len(accounts))


