import unittest

class ConverstionStoreAsserts(unittest.TestCase):

    def assert_conversation_storage(self, store, can_empty=True, test_load=True):

        if can_empty is True:
            store.empty()

        store.store_conversation("client1", "user1", "bot1", "brain1", 0, "HELLO", "Hi there!")
        store.commit()

        if test_load is True:
            conversations = store.load_conversation("client1", "user1")
            self.assertIsNotNone(conversations)
            self.assertEquals(1, len(conversations))