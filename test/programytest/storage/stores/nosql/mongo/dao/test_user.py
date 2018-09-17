import unittest

from programy.storage.stores.nosql.mongo.dao.user import User


class UserTests(unittest.TestCase):

    def test_init_no_id(self):
        user = User(userid='user1', client='client1')

        self.assertIsNotNone(user)
        self.assertIsNone(user.id)
        self.assertEqual('user1', user.userid)
        self.assertEqual('client1', user.client)
        self.assertEqual({'client': 'client1', 'userid': 'user1'} , user.to_document())

    def test_init_with_id(self):
        user = User(userid='user1', client='client1')
        user.id = '666'

        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertEqual('666', user.id)
        self.assertEqual('user1', user.userid)
        self.assertEqual('client1', user.client)
        self.assertEqual({'_id': '666', 'client': 'client1', 'userid': 'user1'} , user.to_document())

    def test_from_document(self):
        user1 = User.from_document({'client': 'client1', 'userid': 'user1'})
        self.assertIsNotNone(user1)
        self.assertIsNone(user1.id)
        self.assertEqual('user1', user1.userid)
        self.assertEqual('client1', user1.client)

        user2 = User.from_document({'_id': '666', 'client': 'client1', 'userid': 'user1'})
        self.assertIsNotNone(user2)
        self.assertIsNotNone(user2.id)
        self.assertEqual('666', user2.id)
        self.assertEqual('user1', user2.userid)
        self.assertEqual('client1', user2.client)
