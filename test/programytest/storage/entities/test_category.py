import unittest

from programy.storage.entities.category import CategoryReadWriteStore


class CategoryStoreTests(unittest.TestCase):

    def test_store_category(self):
        category_store = CategoryReadWriteStore()
        with self.assertRaises(NotImplementedError):
            category_store.store_category("groupid", "userid", "topic", "that", "pattern", "template")
