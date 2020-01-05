import unittest
import unittest.mock
from programy.storage.entities.rdf import RDFReadOnlyStore
from programy.storage.entities.rdf import RDFReadWriteStore


class RDFStoreTests(unittest.TestCase):

    def test_get_split_char(self):
        store = RDFReadOnlyStore()
        self.assertEqual(":", store.get_split_char())

    def test_split_into_fields(self):
        store = RDFReadOnlyStore()
        fields = store.split_into_fields("FIELD1")
        self.assertEquals(["FIELD1"], fields)
        fields = store.split_into_fields("FIELD1!FIELD2")
        self.assertEquals(["FIELD1!FIELD2"], fields)
        fields = store.split_into_fields("FIELD1:FIELD2")
        self.assertEquals(["FIELD1", "FIELD2"], fields)
        fields = store.split_into_fields("FIELD1:FIELD2:FIELD3:FIELD4")
        self.assertEquals(["FIELD1", "FIELD2", "FIELD3:FIELD4"], fields)

    def test_split_line_by_char(self):
        store = RDFReadOnlyStore()
        fields = store.split_line_by_char("FIELD1")
        self.assertEquals(["FIELD1"], fields)
        fields = store.split_line_by_char("FIELD1!FIELD2")
        self.assertEquals(["FIELD1!FIELD2"], fields)
        fields = store.split_line_by_char("FIELD1:FIELD2")
        self.assertEquals(["FIELD1", "FIELD2"], fields)
        fields = store.split_line_by_char("FIELD1:FIELD2:FIELD3:FIELD4")
        self.assertEquals(["FIELD1", "FIELD2", "FIELD3", "FIELD4"], fields)


class RDFReadOnlyStoreTests(unittest.TestCase):

    def test_load(self):
        store = RDFReadOnlyStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

    def test_load_all(self):
        store = RDFReadOnlyStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)


class MockRDFReadWriteStore(RDFReadWriteStore):

    def __init__(self):
        RDFReadWriteStore.__init__(self)
        self.added = False

    def add_rdf(self, name, subject, predicate, objct, replace_existing=True):
        self.added = True


class RDFReadWriteStoreTests(unittest.TestCase):

    def test_process_line(self):
        store = MockRDFReadWriteStore()
        self.assertFalse(store.added)
        store.process_line("TESTRDF",["subject1", "predicate1", "object1"])
        self.assertTrue(store.added)

    def test_process_line_no_fields(self):
        store = MockRDFReadWriteStore()
        self.assertFalse(store.added)
        self.assertFalse(store.process_line("TESTRDF", []))
        self.assertFalse(store.added)

    def test_load(self):
        store = RDFReadWriteStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

    def test_load_all(self):
        store = RDFReadWriteStore()
        with self.assertRaises(NotImplementedError):
            collector = unittest.mock.Mock()
            store.load(collector)

    def test_add_rdf(self):
        store = RDFReadWriteStore()
        with self.assertRaises(NotImplementedError):
            name = unittest.mock.Mock()
            subject = unittest.mock.Mock()
            predicate = unittest.mock.Mock()
            objct = unittest.mock.Mock()
            store.add_rdf(name, subject, predicate, objct)
