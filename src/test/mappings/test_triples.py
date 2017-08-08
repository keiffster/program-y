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
