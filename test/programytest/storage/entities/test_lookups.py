import unittest
import unittest.mock

from programy.storage.entities.lookups import LookupsStore


class LookupsStoreTests(unittest.TestCase):

    def test_load_all(self):
        category_store = LookupsStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            category_store.load_all(collector)

    def test_load(self):
        category_store = LookupsStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            category_store.load(collector)


