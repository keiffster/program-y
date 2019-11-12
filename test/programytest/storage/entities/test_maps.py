import unittest
import unittest.mock
from programy.storage.entities.maps import MapsReadOnlyStore
from programy.storage.entities.maps import MapsReadWriteStore


class MapsStoreTests(unittest.TestCase):

    def test_split_into_fields(self):
        pass


class MapsReadOnlyStoreTests(unittest.TestCase):

    def test_load(self):
        store = MapsReadOnlyStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

    def test_load_all(self):
        store = MapsReadOnlyStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)


class MapsReadWriteStoreTests(unittest.TestCase):

    def test_process_line(self):
        pass

    def test_load(self):
        store = MapsReadWriteStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

    def test_load_all(self):
        store = MapsReadWriteStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

    def test_add_to_map(self):
        store = MapsReadWriteStore()
        with self.assertRaises(NotImplementedError):
            name = unittest.mock.Mock()
            key = unittest.mock.Mock()
            value = unittest.mock.Mock()
            store.add_to_map(name, key, value)

    def test_remove_from_map(self):
        store = MapsReadWriteStore()
        with self.assertRaises(NotImplementedError):
            name = unittest.mock.Mock()
            key = unittest.mock.Mock()
            store.remove_from_map(name, key)
