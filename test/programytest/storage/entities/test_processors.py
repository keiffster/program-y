import unittest
import unittest.mock

from programy.storage.entities.processors import ProcessorStore


class ProcessorsStoreTests(unittest.TestCase):

    def test_load(self):
        store = ProcessorStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

