import unittest

from programy.rdf.collection import RDFCollection


class RDFCollectionTests(unittest.TestCase):

    def test_rdf_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        count = collection.load_from_text("""
            ACCOUNT:hasPurpose:to track money
            ACCOUNT:hasSize:0
            ACCOUNT:hasSyllables:2
            ACCOUNT:isa:Concept
            ACCOUNT:lifeArea:Finances
            ACT:hasPurpose:to entertain by performing
        """)
        self.assertEqual(count, 6)

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'isa', 'Concept'))

        self.assertFalse(collection.has_subject('ACCOUNTX'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSizeX'))
        self.assertFalse(collection.has_object('ACCOUNT', 'isa', 'ConceptX'))

    def test_add_rdf_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_rdf_collection_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize", "0")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_rdf_collection_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_rdf_collection_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT")

        self.assertFalse(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_subjects(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("MONKEY", "legs", "2")
        collection.add_entity("ZEBRA", "legs", "4")

        subjects = collection.subjects()
        self.assertEquals(2, len(subjects))
        self.assertTrue("MONKEY" in subjects)
        self.assertTrue("ZEBRA" in subjects)

    def test_predicates(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("MONKEY", "legs", "2")
        collection.add_entity("ZEBRA", "legs", "4")

        predicates = collection.predicates("MONKEY")
        self.assertEquals(1, len(predicates))
        self.assertEquals("legs", predicates[0])

    def test_objects(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("MONKEY", "legs", "2")
        collection.add_entity("MONKEY", "hasFur", "true")
        collection.add_entity("ZEBRA", "legs", "4")
        collection.add_entity("BIRD", "legs", "2")
        collection.add_entity("ELEPHANT", "trunk", "true")

        subjects = collection.subjects()
        self.assertEquals(4, len(subjects))

        object = collection.objects(subject="MONKEY", predicate="legs")
        self.assertEqual(["2"], object)

    def add_data(self, collection):
        collection.add_entity("MONKEY", "legs", "2")
        collection.add_entity("MONKEY", "hasFur", "true")
        collection.add_entity("ZEBRA", "legs", "4")
        collection.add_entity("BIRD", "legs", "2")
        collection.add_entity("ELEPHANT", "trunk", "true")

    def test_match_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.match(subject="MONKEY")
        self.assertEquals(2, len(matches))
        self.assertEqual("MONKEY", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("2", matches[0].object)
        self.assertEqual("MONKEY", matches[1].subject)
        self.assertEqual("hasFur", matches[1].predicate)
        self.assertEqual("true", matches[1].object)

    def test_match_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.match(predicate="legs")
        self.assertEquals(3, len(matches))
        self.assertEqual("MONKEY", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("2", matches[0].object)
        self.assertEqual("ZEBRA", matches[1].subject)
        self.assertEqual("legs", matches[1].predicate)
        self.assertEqual("4", matches[1].object)
        self.assertEqual("BIRD", matches[2].subject)
        self.assertEqual("legs", matches[2].predicate)
        self.assertEqual("2", matches[2].object)

    def test_match_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.match(subject="MONKEY", predicate="legs")
        self.assertEquals(1, len(matches))
        self.assertEqual("MONKEY", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("2", matches[0].object)

    def test_match_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.match(predicate="legs", object="2")
        self.assertEquals(2, len(matches))
        self.assertEqual("MONKEY", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("2", matches[0].object)
        self.assertEqual("BIRD", matches[1].subject)
        self.assertEqual("legs", matches[1].predicate)
        self.assertEqual("2", matches[1].object)

    def test_match_subject_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.match(subject="MONKEY", object="2")
        self.assertEquals(1, len(matches))
        self.assertEqual("MONKEY", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("2", matches[0].object)

    def test_match_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.match(object="2")
        self.assertEquals(2, len(matches))
        self.assertEqual("MONKEY", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("2", matches[0].object)
        self.assertEqual("BIRD", matches[1].subject)
        self.assertEqual("legs", matches[1].predicate)
        self.assertEqual("2", matches[1].object)

    def test_not_match(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.not_match()
        self.assertEquals(0, len(matches))

    def test_not_match_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.not_match(subject="MONKEY")
        self.assertEquals(3, len(matches))

    def test_not_match_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.not_match(predicate="legs")
        self.assertEquals(1, len(matches))
        self.assertEqual("ELEPHANT", matches[0].subject)
        self.assertEqual("trunk", matches[0].predicate)
        self.assertEqual("true", matches[0].object)

    def test_not_match_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.not_match(object="4")
        self.assertEquals(4, len(matches))
        self.assertEqual("MONKEY", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("2", matches[0].object)
        self.assertEqual("MONKEY", matches[1].subject)
        self.assertEqual("hasFur", matches[1].predicate)
        self.assertEqual("true", matches[1].object)
        self.assertEqual("BIRD", matches[2].subject)
        self.assertEqual("legs", matches[2].predicate)
        self.assertEqual("2", matches[2].object)
        self.assertEqual("ELEPHANT", matches[3].subject)
        self.assertEqual("trunk", matches[3].predicate)
        self.assertEqual("true", matches[3].object)

    def test_not_match_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.not_match(subject="MONKEY", predicate="legs")

        self.assertEquals(3, len(matches))
        self.assertEqual("ZEBRA", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("4", matches[0].object)
        self.assertEqual("BIRD", matches[1].subject)
        self.assertEqual("legs", matches[1].predicate)
        self.assertEqual("2", matches[1].object)
        self.assertEqual("ELEPHANT", matches[2].subject)
        self.assertEqual("trunk", matches[2].predicate)
        self.assertEqual("true", matches[2].object)

    def test_not_match_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.not_match(predicate="legs", object="2")
        self.assertEquals(2, len(matches))
        self.assertEqual("ZEBRA", matches[0].subject)
        self.assertEqual("legs", matches[0].predicate)
        self.assertEqual("4", matches[0].object)
        self.assertEqual("ELEPHANT", matches[1].subject)
        self.assertEqual("trunk", matches[1].predicate)
        self.assertEqual("true", matches[1].object)

    def test_not_match_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)
        self.add_data(collection)

        matches = collection.not_match(subject="MONKEY", predicate="legs", object="2")
        self.assertEquals(3, len(matches))

