import unittest
import unittest.mock
from programy.storage.entities.maps import MapsReadOnlyStore
from programy.storage.entities.maps import MapsReadWriteStore


class MapsStoreTests(unittest.TestCase):

    def test_get_split_char(self):
        store = MapsReadOnlyStore()
        self.assertEqual(":", store.get_split_char())

    def test_split_into_fields(self):
        store = MapsReadOnlyStore()
        fields = store.split_into_fields("FIELD1")
        self.assertEquals(["FIELD1", ''], fields)
        fields = store.split_into_fields("FIELD1!FIELD2")
        self.assertEquals(["FIELD1!FIELD2", ''], fields)
        fields = store.split_into_fields("FIELD1:FIELD2")
        self.assertEquals(["FIELD1", "FIELD2"], fields)
        fields = store.split_into_fields("FIELD1:FIELD2:FIELD3:FIELD4")
        self.assertEquals(["FIELD1", "FIELD2:FIELD3:FIELD4"], fields)


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


class MockMapsReadWriteStore(MapsReadWriteStore):

    def __init__(self):
        MapsReadWriteStore.__init__(self)
        self.added = False

    def add_to_map(self, name, key, value, overwrite_existing=False):
        self.added = True


class MapsReadWriteStoreTests(unittest.TestCase):

    def test_process_line(self):
        store = MockMapsReadWriteStore()
        store.process_line("MAP1", ["NAME", "VALUE"])
        self.assertTrue(store.added)

    def test_process_line_no_fields(self):
        store = MockMapsReadWriteStore()
        self.assertFalse(store.process_line("MAP1", []))
        self.assertFalse(store.added)

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
