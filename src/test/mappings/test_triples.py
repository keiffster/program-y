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
        self.assertTrue(collection.has_objective('ACCOUNT', 'isa', 'Concept'))
        self.assertEquals("Concept", collection.objective('ACCOUNT', 'isa'))

        self.assertFalse(collection.has_subject('ACCOUNTX'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSizeX'))
        self.assertFalse(collection.has_objective('ACCOUNT', 'isa', 'ConceptX'))

    def test_add_triples(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_objective('ACCOUNT', 'hasSize', "0"))

    def test_delete_triples_subject_predicate_objective(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_objective('ACCOUNT', 'hasSize', "0"))

        collection.delete_triple("ACCOUNT", "hasSize", "0")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_objective('ACCOUNT', 'hasSize', "0"))

    def test_delete_triples_subject_predicate(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_objective('ACCOUNT', 'hasSize', "0"))

        collection.delete_triple("ACCOUNT", "hasSize")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_objective('ACCOUNT', 'hasSize', "0"))

    def test_delete_triples_subject(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_objective('ACCOUNT', 'hasSize', "0"))

        collection.delete_triple("ACCOUNT")

        self.assertFalse(collection.has_subject('ACCOUNT'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertFalse(collection.has_objective('ACCOUNT', 'hasSize', "0"))

    def test_subjects(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("ZEBRA", "legs", "4")

        subjects = collection.subjects()
        self.assertEquals(2, len(subjects))
        self.assertTrue("MONKEY" in subjects)
        self.assertTrue("ZEBRA" in subjects)

    def test_predicates(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("ZEBRA", "legs", "4")

        predicates = collection.predicates()
        self.assertEquals(2, len(predicates))

        predicates = collection.predicates("MONKEY")
        self.assertEquals(1, len(predicates))

    def test_objectives(self):

        collection = TriplesCollection()
        self.assertIsNotNone(collection)

        collection.add_triple("MONKEY", "legs", "2")
        collection.add_triple("MONKEY", "hasFur", "true")
        collection.add_triple("ZEBRA", "legs", "4")
        collection.add_triple("BIRD", "legs", "2")
        collection.add_triple("ELEPHANT", "trunk", "true")

        objectives = collection.objectives()
        self.assertEquals(5, len(objectives))

        objectives = collection.objectives(predicate_name="legs")
        self.assertEquals(3, len(objectives))

        objectives = collection.objectives(predicate_name="legs")
        self.assertEquals(3, len(objectives))

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

        matches = collection.match(predicate_name="legs", objective_name="2")
        self.assertEquals(2, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])
        self.assertEqual(["BIRD", "legs", "2"], matches[1])

        matches = collection.match(subject_name="MONKEY", objective_name="2")
        self.assertEquals(1, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])

        matches = collection.match(objective_name="2")
        self.assertEquals(2, len(matches))
        self.assertEqual(["MONKEY", "legs", "2"], matches[0])
        self.assertEqual(["BIRD", "legs", "2"], matches[1])
