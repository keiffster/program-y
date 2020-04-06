import unittest
import unittest.mock

from programy.storage.entities.services import ServicesStore


class ServicesStoreTest(unittest.TestCase):

    def test_load(self):
        store = ServicesStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

