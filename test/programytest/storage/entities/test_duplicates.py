import unittest
import unittest.mock

from programy.storage.entities.duplicates import DuplicatesStore


class DuplicatesStoreTests(unittest.TestCase):

    def test_save_duplicates(self):
        store = DuplicatesStore()
        with self.assertRaises(NotImplementedError):
            duplicates = unittest.mock.Mock()
            store.save_duplicates(duplicates)
