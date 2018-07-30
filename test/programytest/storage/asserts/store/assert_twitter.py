import unittest

class TwitterStoreAsserts(unittest.TestCase):

    def assert_twitter_storage(self, store):

        store.empty()

        last_direct_message_id, last_status_id = store.load_last_message_ids()

        self.assertEquals(last_direct_message_id, -1)
        self.assertEquals(last_status_id, -1)

        store.store_last_message_ids(666, 999)

        last_direct_message_id, last_status_id = store.load_last_message_ids()

        self.assertEquals(last_direct_message_id, 666)
        self.assertEquals(last_status_id, 999)
