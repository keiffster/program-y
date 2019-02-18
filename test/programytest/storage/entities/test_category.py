import unittest

from programy.storage.entities.category import CategoryStore

class CategoryStoreTests(unittest.TestCase):

    def test_store_category(self):
        category_store = CategoryStore()
        with self.assertRaises(NotImplementedError):
            category_store.store_category("groupid", "userid", "topic", "that", "pattern", "template")
