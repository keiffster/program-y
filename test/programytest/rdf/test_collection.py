import unittest

from programy.rdf.collection import RDFCollection


class RDFCollectionTests(unittest.TestCase):

    def test_properties(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.assertEquals({}, collection.entities)
        self.assertEquals({}, collection.entities_to_ids)
        self.assertEquals({}, collection.stores)
        self.assertEquals({}, collection.entities_to_stores)

        self.assertEquals([], collection.subjects())
        self.assertEquals([], collection.predicates('ACCOUNT'))
        self.assertEquals([], collection.objects('ACCOUNT', 'HASSIZE'))

        self.assertIsNone(collection.storename("BANKING"))

    def test_add_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))
        self.assertIsNone(collection.storename("BANKING"))

        self.assertFalse(collection.has_object('ACCOUNTX', 'hasSize', "0"))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSizeX', "0"))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "§"))

        self.assertEquals(['ACCOUNT'], collection.subjects())
        self.assertEquals(['HASSIZE'], collection.predicates('ACCOUNT'))
        self.assertEquals([], collection.predicates('ACCOUNTXX'))
        self.assertEquals([['0']], collection.objects('ACCOUNT', 'HASSIZE'))
        self.assertEquals([], collection.objects('ACCOUNT', 'HASSIZEXX'))

    def test_add_collection_with_rdfstore_entityid(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", rdf_store="file", entityid="1")

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        self.assertFalse(collection.has_object('ACCOUNTX', 'hasSize', "0"))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSizeX', "0"))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "§"))

        self.assertEquals("file", collection.storename("BANKING"))
        self.assertEquals("BANKING", collection.entities_to_stores["ACCOUNT"])
        entities = collection.entities_to_ids["1"]
        self.assertIsNotNone(entities)
        self.assertEquals(1, len(entities))
        self.assertEquals({'HASSIZE': ['0', '0']}, entities[0].predicates)

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

    def test_delete_collection_subject_not_exists(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNTX")

        self.assertTrue(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize")

        self.assertFalse(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate_no_exists_no_obj(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSizeX")

        self.assertTrue(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate_no_exists_with_obj(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANIKING")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSizeX", "0")

        self.assertTrue(collection.has_subject('ACCOUNT'))

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

    def test_add_collection_multiple_with_entityid(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", entityid="1")
        collection.add_entity("ACCOUNT", "hasValue", "1", "BANKING", entityid="1")

        self.assertEquals("BANKING", collection.entities_to_stores["ACCOUNT"])
        entities = collection.entities_to_ids["1"]
        self.assertIsNotNone(entities)
        self.assertEquals(1, len(entities))
        self.assertEquals({'HASSIZE': ['0'], 'HASVALUE': ['1']}, entities[0].predicates)

    def test_add_collection_multiple_with_entityid2(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", "BANKING", entityid="1")
        collection.add_entity("BALANCE", "hasValue", "1", "BANKING", entityid="1")

        self.assertEquals("BANKING", collection.entities_to_stores["ACCOUNT"])
        entities = collection.entities_to_ids["1"]
        self.assertIsNotNone(entities)
        self.assertEquals(2, len(entities))
        self.assertEquals({'HASSIZE': ['0']}, entities[0].predicates)
        self.assertEquals({'HASVALUE': ['1']}, entities[1].predicates)

    def test_empty_all(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", rdf_name="BANKING", rdf_store="TEST", entityid="1")
        collection.add_entity("BALANCE", "hasValue", "1", rdf_name="BANKING", rdf_store="TEST", entityid="2")

        collection.add_entity("WALKING", "hasSize", "0", rdf_name="ACTIVITY", rdf_store="TEST", entityid="3")
        collection.add_entity("RUNNING", "hasValue", "1", rdf_name="ACTIVITY", rdf_store="TEST", entityid="4")

        self.assertEquals("BANKING", collection.entities_to_stores['ACCOUNT'])
        self.assertEquals("ACTIVITY", collection.entities_to_stores['RUNNING'])

        self.assertTrue(collection.contains('BANKING'))
        self.assertTrue(collection.contains('ACTIVITY'))

        collection.empty()

        self.assertFalse(collection.contains('BANKING'))
        self.assertFalse(collection.contains('ACTIVITY'))

    def test_empty_by_name(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0", rdf_name="BANKING", rdf_store="TEST", entityid="1")
        collection.add_entity("BALANCE", "hasValue", "1", rdf_name="BANKING", rdf_store="TEST", entityid="2")

        collection.add_entity("WALKING", "hasSize", "0", rdf_name="ACTIVITY", rdf_store="TEST", entityid="3")
        collection.add_entity("RUNNING", "hasValue", "1", rdf_name="ACTIVITY", rdf_store="TEST", entityid="4")

        self.assertEquals("BANKING", collection.entities_to_stores['ACCOUNT'])
        self.assertEquals("ACTIVITY", collection.entities_to_stores['RUNNING'])

        self.assertTrue(collection.contains('BANKING'))
        self.assertTrue(collection.contains('ACTIVITY'))

        collection.empty("BANKING")

        self.assertFalse(collection.contains('BANKING'))
        self.assertTrue(collection.contains('ACTIVITY'))
