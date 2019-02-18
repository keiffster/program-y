import unittest

from programy.rdf.collection import RDFCollection


class RDFCollectionCreationTests(unittest.TestCase):

    def test_add_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_add_multi_object_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACTOR", "ISA", "PERSON", "TEST")
        collection.add_entity("ACTOR", "ISA", "MAN", "TEST")

        self.assertTrue(collection.has_subject('ACTOR'))

        self.assertTrue(collection.has_predicate('ACTOR', 'ISA'))

        self.assertTrue(collection.has_object('ACTOR', 'ISA', "PERSON"))
        self.assertTrue(collection.has_object('ACTOR', 'ISA', "MAN"))

    def test_delete_collection_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT")

        self.assertFalse(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize")

        self.assertFalse(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize", "0")

        self.assertFalse(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_collection_subject_predicate_diff_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize", "1")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

