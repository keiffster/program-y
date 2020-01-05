import unittest.mock

from programy.storage.entities.twitter import TwitterStore


class TwitterStoreTests(unittest.TestCase):

    def test_store_last_message_ids(self):
        store = TwitterStore()
        with self.assertRaises(NotImplementedError):
            store.store_last_message_ids(1, 2)

    def test_load_last_message_ids(self):
        store = TwitterStore()
        with self.assertRaises(NotImplementedError):
            store.load_last_message_ids()
