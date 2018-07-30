import unittest

from programy.storage.entities.linked import LinkedAccountStore

class LinkedAccountStoreTests(unittest.TestCase):

    def test_link_accounts(self):
        linked_store = LinkedAccountStore()
        with self.assertRaises(NotImplementedError):
            linked_store.link_accounts("primary_userid", "linked_userid")
