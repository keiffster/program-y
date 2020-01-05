import unittest
import unittest.mock

from programy.storage.entities.license import LicenseStore


class LicenseStoreTests(unittest.TestCase):

    def test_load_all(self):
        store = LicenseStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock
            store.load_all(collector)

    def test_load(self):
        store = LicenseStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock
            store.load(collector)
