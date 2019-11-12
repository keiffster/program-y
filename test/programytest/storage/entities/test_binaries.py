import unittest
import unittest.mock

from programy.storage.entities.binaries import BinariesStore


class BinariesStoreTests(unittest.TestCase):

    def test_save_binary(self):
        store = BinariesStore()
        with self.assertRaises(NotImplementedError):
            aiml_parser = unittest.mock.Mock()
            store.save_binary(aiml_parser)

    def test_load_binary(self):
        store = BinariesStore()
        with self.assertRaises(NotImplementedError):
            store.load_binary()



