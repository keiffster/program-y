import unittest

from programy.storage.entities.defaults import DefaultStore


class DefaultStoreTests(unittest.TestCase):

    def test_add_default(self):
        default_store = DefaultStore()
        with self.assertRaises(NotImplementedError):
            default_store.add_default("name", "value")

    def test_add_properties(self):
        default_store = DefaultStore()
        with self.assertRaises(NotImplementedError):
            default_store.add_defaults({"name1", "val1"})
