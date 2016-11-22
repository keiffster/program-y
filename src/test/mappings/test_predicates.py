import unittest

from programy.mappings.predicates import PredicatesCollection


class PredicateTests(unittest.TestCase):

    def test_collection(self):
        collection = PredicatesCollection()
        self.assertIsNotNone(collection)

        count = collection.load_from_text("""
            address:where
            age:how many
            baby:who
            bestfriend:who
            birthday:when
            birthplace:where
            boyfriend:who
            """)
        self.assertEqual(count, 7)
        self.assertEqual(collection.predicate("baby"), "who")