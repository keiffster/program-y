import unittest

from programy.storage.stores.nosql.mongo.dao.twitter import Twitter


class TwitterTests(unittest.TestCase):

    def test_init_no_id(self):
        twitter = Twitter(last_direct_message_id='1', last_status_id='2')

        self.assertIsNotNone(twitter)
        self.assertIsNone(twitter.id)
        self.assertEqual('1', twitter.last_direct_message_id)
        self.assertEqual('2', twitter.last_status_id)
        self.assertEqual({'last_direct_message_id': '1', 'last_status_id': '2'}, twitter.to_document())

    def test_init_with_id(self):
        twitter = Twitter(last_direct_message_id='1', last_status_id='2')
        twitter.id = '666'

        self.assertIsNotNone(twitter)
        self.assertIsNotNone(twitter.id)
        self.assertEqual('666', twitter.id)
        self.assertEqual('1', twitter.last_direct_message_id)
        self.assertEqual('2', twitter.last_status_id)
        self.assertEqual({'_id': '666', 'last_direct_message_id': '1', 'last_status_id': '2'}, twitter.to_document())

    def test_from_document(self):
        twitter1 = Twitter.from_document({'last_direct_message_id': '1', 'last_status_id': '2'})
        self.assertIsNone(twitter1.id)
        self.assertEqual('1', twitter1.last_direct_message_id)
        self.assertEqual('2', twitter1.last_status_id)

        twitter2 = Twitter.from_document({'_id': '666', 'last_direct_message_id': '1', 'last_status_id': '2'})
        self.assertIsNotNone(twitter2)
        self.assertIsNotNone(twitter2.id)
        self.assertEqual('666', twitter2.id)
        self.assertEqual('1', twitter2.last_direct_message_id)
        self.assertEqual('2', twitter2.last_status_id)
