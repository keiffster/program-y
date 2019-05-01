import unittest

from programy.storage.entities.property import PropertyStore


class PropertyStoreTests(unittest.TestCase):

    def test_add_property(self):
        property_store = PropertyStore()
        with self.assertRaises(NotImplementedError):
            property_store.add_property("name", "value")

    def test_add_properties(self):
        property_store = PropertyStore()
        with self.assertRaises(NotImplementedError):
            property_store.add_properties({"name1", "val1"})
