import unittest
from programy.storage.entities.category import CategoryReadWriteStore


class CategoryStoreTests(unittest.TestCase):

    def test_extract_content(self):
        pass

    def test_find_all(self):
        pass

    def test_find_element_str(self):
        pass


class CategoryReadOnlyStoreTests(unittest.TestCase):

    def test_load_category(self):
        pass


class CategoryReadWriteStoreTests(unittest.TestCase):

    def test_store_category(self):
        category_store = CategoryReadWriteStore()
        with self.assertRaises(NotImplementedError):
            category_store.store_category("groupid", "userid", "topic", "that", "pattern", "template")

    def test_upload_from_file(self):
        pass


