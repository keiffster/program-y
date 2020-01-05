import unittest
import unittest.mock

from programy.storage.entities.triggers import TriggersStore


class TriggersStoreTests(unittest.TestCase):

    def test_load(self):
        store = TriggersStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)
