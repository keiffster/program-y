import unittest
import unittest.mock

from programy.storage.entities.learnf import LearnfStore


class LearnfStoreTests(unittest.TestCase):

    def test_save_learnf(self):
        store = LearnfStore()
        with self.assertRaises(NotImplementedError):
            client_context = unittest.mock.Mock()
            category = unittest.mock.Mock()
            store.save_learnf(client_context, category)


