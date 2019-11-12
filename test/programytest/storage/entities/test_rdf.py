import unittest
import unittest.mock
from programy.storage.entities.rdf import RDFReadOnlyStore
from programy.storage.entities.rdf import RDFReadWriteStore


class RDFStoreTests(unittest.TestCase):

    def test_get_split_char(self):
        pass

    def test_split_into_fields(self):
        pass

    def test_split_line_by_char(self):
        pass


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


class RDFReadWriteStoreTests(unittest.TestCase):

    def test_process_line(self):
        pass

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
