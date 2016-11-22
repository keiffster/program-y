import unittest

from programy.mappings.triples import TriplesCollection


class TripleTests(unittest.TestCase):

    def test_collection(self):
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

        self.assertIsNotNone(collection.has_primary('ACCOUNT'))
        self.assertIsNotNone(collection.has_secondary('ACCOUNT', 'hasSize'))
        self.assertIsNotNone(collection.has_secondary('ACCOUNT', 'isa'))

