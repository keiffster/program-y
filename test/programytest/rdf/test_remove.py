import unittest

from programy.rdf.collection import RDFCollection


class RDFCollectionRemoveTests(unittest.TestCase):

    def add_data(self, collection):
        collection.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        collection.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        collection.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        collection.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        collection.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

    def test_remove_subject(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY')
        self.assertIsNotNone(remains)
        self.assertEqual(3, len(remains))
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)

    def test_remove_subject_predicate(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY', predicate="LEGS")
        self.assertIsNotNone(remains)
        self.assertEqual(4, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)

    def test_remove_subject_object(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY', obj="2")
        self.assertIsNotNone(remains)
        self.assertEqual(4, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in all)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in all)
        self.assertTrue(["BIRD", "LEGS", "2"] in all)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in all)

    def test_remove_predicate(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, predicate='LEGS')
        self.assertIsNotNone(remains)
        self.assertEqual(2, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)

    def test_remove_predicate_object(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, predicate='LEGS', obj="2")
        self.assertIsNotNone(remains)
        self.assertEqual(3, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in all)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in all)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in all)

    def test_remove_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, obj='2')
        self.assertIsNotNone(remains)
        self.assertEqual(3, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)

    def test_remove_subject_predicate_object(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY', predicate="LEGS", obj="2")
        self.assertIsNotNone(remains)
        self.assertEqual(4, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)

    def test_remove_nothing(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all)
        self.assertIsNotNone(remains)
        self.assertEqual(5, len(remains))
        self.assertTrue(["MONKEY", "LEGS", "2"] in remains)
        self.assertTrue(["MONKEY", "HASFUR", "true"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)
