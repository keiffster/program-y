import unittest

from programy.storage.entities.conversation import ConversationStore


class ConversationStoreTests(unittest.TestCase):

    def test_store_conversation(self):
        convo_store = ConversationStore()
        with self.assertRaises(NotImplementedError):
            convo_store.store_conversation("clientid", "userid", "botid", "brainid", "depth", "question", "response")
