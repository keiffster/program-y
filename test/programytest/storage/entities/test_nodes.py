import unittest
import unittest.mock

from programy.storage.entities.nodes import NodesStore


class NodesStoreTest(unittest.TestCase):

    def test_load(self):
        store = NodesStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

