import unittest

from programy.storage.stores.nosql.mongo.dao.linked import LinkedAccount


class LinkedAccountTests(unittest.TestCase):

    def test_init_no_id(self):
        linked = LinkedAccount(primary_userid='user1', linked_userid='user2')

        self.assertIsNotNone(linked)
        self.assertIsNone(linked.id)
        self.assertEqual('user1', linked.primary_userid)
        self.assertEqual('user2', linked.linked_userid)
        self.assertEqual({'linked_userid': 'user2', 'primary_userid': 'user1'}, linked.to_document())

    def test_init_with_id(self):
        linked = LinkedAccount(primary_userid='user1', linked_userid='user2')
        linked.id = '666'

        self.assertIsNotNone(linked)
        self.assertIsNotNone(linked.id)
        self.assertEqual('666', linked.id)
        self.assertEqual('user1', linked.primary_userid)
        self.assertEqual('user2', linked.linked_userid)
        self.assertEqual({'_id': '666', 'linked_userid': 'user2', 'primary_userid': 'user1'}, linked.to_document())

    def test_from_document(self):
        linked1 = LinkedAccount.from_document({'linked_userid': 'user2', 'primary_userid': 'user1'})
        self.assertIsNotNone(linked1)
        self.assertIsNone(linked1.id)
        self.assertEqual('user1', linked1.primary_userid)
        self.assertEqual('user2', linked1.linked_userid)

        linked2 = LinkedAccount.from_document({'_id': '666', 'linked_userid': 'user2', 'primary_userid': 'user1'})
        self.assertIsNotNone(linked2)
        self.assertIsNotNone(linked2.id)
        self.assertEqual('666', linked2.id)
        self.assertEqual('user1', linked2.primary_userid)
        self.assertEqual('user2', linked2.linked_userid)
