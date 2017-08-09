import unittest

from programy.mappings.triples import TriplesCollection


class TripleTests(unittest.TestCase):

    def test_triples(self):
        collection = TriplesCollection()
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
        self.assertEquals("Concept", collection.object('ACCOUNT', 'isa'))

        self.assertFalse(collection.has_subject('ACCOUNTX'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSizeX'))
        self.assertFalse(collection.has_object('ACCOUNT', 'isa', 'ConceptX'))

    def test_add_triples(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_triples_subject_predicate_object(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_triple("ACCOUNT", "hasSize", "0")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_triples_subject_predicate(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_triple("ACCOUNT", "hasSize")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_triples_subject(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_triple("ACCOUNT")

        self.assertFalse(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_subjects(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("ZEBRA", "legs", "4")

        subjects = collection.subjects()
        self.assertEquals(2, len(subjects))
        self.assertTrue("MONKEY" in subjects)
        self.assertTrue("ZEBRA" in subjects)

        subjects = collection.subjects(subject_name="MONKEY")
        self.assertEquals(1, len(subjects))
        self.assertTrue("MONKEY" in subjects)

    def test_predicates(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("ZEBRA", "legs", "4")

        predicates = collection.predicates()
        self.assertEquals(2, len(predicates))
        self.assertEquals(["MONKEY", "legs"], predicates[0])
        self.assertEquals(["ZEBRA", "legs"], predicates[1])

        predicates = collection.predicates(subject_name="MONKEY")
        self.assertEquals(1, len(predicates))
        self.assertEquals(["MONKEY", "legs"], predicates[0])

        predicates = collection.predicates(predicate_name="legs")
        self.assertEquals(2, len(predicates))
        self.assertEquals(["MONKEY", "legs"], predicates[0])
        self.assertEquals(["ZEBRA", "legs"], predicates[1])

    def test_objects(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("MONKEY", "hasFur", "true")
        collection.add_triple("ZEBRA", "legs", "4")
        collection.add_triple("BIRD", "legs", "2")
        collection.add_triple("ELEPHANT", "trunk", "true")

        objects = collection.objects()
        self.assertEquals(5, len(objects))

        objects = collection.objects(predicate_name="legs")
        self.assertEquals(3, len(objects))

    def test_match(self):
        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("MONKEY", "hasFur", "true")
        collection.add_triple("ZEBRA", "legs", "4")
        collection.add_triple("BIRD", "legs", "2")
        collection.add_triple("ELEPHANT", "trunk", "true")

        matches = collection.match(subject_name="MONKEY")
        self.assertEquals(2, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])
        self.assertEqual(["MONKEY", "hasFur", "true"], matches[1])

        matches = collection.match(predicate_name="legs")
        self.assertEquals(3, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])
        self.assertEqual(["ZEBRA", "legs", "4"], matches[1])
        self.assertEqual(["BIRD", "legs", "2"], matches[2])

        matches = collection.match(subject_name="MONKEY", predicate_name="legs")
        self.assertEquals(1, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])

        matches = collection.match(predicate_name="legs", object_name="2")
        self.assertEquals(2, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])
        self.assertEqual(["BIRD", "legs", "2"], matches[1])

        matches = collection.match(subject_name="MONKEY", object_name="2")
        self.assertEquals(1, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])

        matches = collection.match(object_name="2")
        self.assertEquals(2, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])
        self.assertEqual(["BIRD", "legs", "2"], matches[1])

    def test_not_match(self):
        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("MONKEY", "hasFur", "true")
        collection.add_triple("ZEBRA", "legs", "4")
        collection.add_triple("BIRD", "legs", "2")
        collection.add_triple("ELEPHANT", "trunk", "true")

        matches = collection.not_match(subject_name="MONKEY")
        self.assertEquals(3, len(matches))

        matches = collection.not_match(predicate_name="legs")
        self.assertEquals(2, len(matches))

        matches = collection.not_match(object_name="4")
        self.assertEquals(4, len(matches))

        matches = collection.not_match(subject_name="MONKEY", predicate_name="legs")
        self.assertEquals(1, len(matches))

        matches = collection.not_match(subject_name="MONKEY", object_name="2")
        self.assertEquals(2, len(matches))

        matches = collection.not_match(predicate_name="legs", object_name="2")
        self.assertEquals(2, len(matches))

    def test_matching(self):
        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("MONKEY", "hasFur", "true")
        collection.add_triple("ZEBRA", "legs", "4")
        collection.add_triple("BIRD", "legs", "2")
        collection.add_triple("ELEPHANT", "trunk", "true")

        for subject in collection.triples.keys():
            for predicate in collection.triples[subject].keys():
                object = collection.triples[subject][predicate]
                print("%10s, %10s, %10s"%(subject, predicate, object))

