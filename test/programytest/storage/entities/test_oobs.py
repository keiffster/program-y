import unittest
import unittest.mock

from programy.storage.entities.oobs import OOBsStore


class OOBsStoreTest(unittest.TestCase):

    def test_load(self):
        store = OOBsStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

