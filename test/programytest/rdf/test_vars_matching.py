import unittest

from programy.rdf.collection import RDFCollection


class RDFCollectionVarsMatchingTests(unittest.TestCase):

    def add_data(self, collection):
        collection.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        collection.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        collection.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        collection.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        collection.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

    def test_match_vars(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars()
        self.assertIsNotNone(matched)
        self.assertEqual(5, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'HASFUR'], ['obj', 'true']] in matched)
        self.assertTrue([['subj', 'ELEPHANT'], ['pred', 'TRUNK'], ['obj', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['pred', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars()
        self.assertIsNotNone(matched)
        self.assertEqual(0, len(matched))

    def test_match_vars_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars("?x")
        self.assertIsNotNone(matched)
        self.assertEqual(5, len(matched))
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'HASFUR'], ['obj', 'true']] in matched)
        self.assertTrue([['?x', 'ELEPHANT'], ['pred', 'TRUNK'], ['obj', 'true']] in matched)
        self.assertTrue([['?x', 'ZEBRA'], ['pred', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        not_matched = collection.not_match_to_vars("?x")
        self.assertIsNotNone(not_matched)
        self.assertEqual(0, len(not_matched))

    def test_match_vars_subject_with_predicate_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="?x", predicate="LEGS")
        self.assertIsNotNone(matched)
        self.assertEqual(3, len(matched))
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['?x', 'ZEBRA'], ['pred', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars_subject_with_predicate_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        not_matched = collection.not_match_to_vars(subject="?x", predicate="LEGS")
        self.assertIsNotNone(not_matched)
        self.assertEqual(1, len(not_matched))
        self.assertTrue([['?x', 'ELEPHANT'], ['pred', 'TRUNK'], ['obj', 'true']] in not_matched)

    def test_match_vars_subject_with_predicate_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="?x", predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEqual(2, len(matched))
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars_subject_with_predicate_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="?x", predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEqual(2, len(matched))
        self.assertTrue([['?x', 'ZEBRA'], ['pred', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['?x', 'ELEPHANT'], ['pred', 'TRUNK'], ['obj', 'true']] in matched)

    def test_match_vars_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="?x", predicate="?y")
        self.assertIsNotNone(matched)
        self.assertTrue([['?x', 'MONKEY'], ['?y', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['?x', 'MONKEY'], ['?y', 'HASFUR'], ['obj', 'true']] in matched)
        self.assertTrue([['?x', 'ELEPHANT'], ['?y', 'TRUNK'], ['obj', 'true']] in matched)
        self.assertTrue([['?x', 'ZEBRA'], ['?y', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['?y', 'LEGS'], ['obj', '2']] in matched)

    def test_match_vars_subject_predicate_with_subject_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="MONKEY", predicate="?y")
        self.assertIsNotNone(matched)
        self.assertEqual(2, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['?y', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['?y', 'HASFUR'], ['obj', 'true']] in matched)

    def test_not_match_vars_subject_predicate_with_subject_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="MONKEY", predicate="?y")
        self.assertIsNotNone(matched)
        self.assertEqual(3, len(matched))
        self.assertTrue([['subj', 'ZEBRA'], ['?y', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['?y', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['subj', 'ELEPHANT'], ['?y', 'TRUNK'], ['obj', 'true']] in matched)

    def test_match_vars_subject_predicate_with_subject_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="MONKEY", predicate="?y", obj="2")
        self.assertIsNotNone(matched)
        self.assertEqual(1, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['?y', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars_subject_predicate_with_subject_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="MONKEY", predicate="?y", obj="2")
        self.assertIsNotNone(matched)
        self.assertEqual(3, len(matched))
        self.assertTrue([['subj', 'ELEPHANT'], ['?y', 'TRUNK'], ['obj', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['?y', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['?y', 'LEGS'], ['obj', '2']] in matched)

    def test_match_vars_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars("?x", "?y", "?z")
        self.assertIsNotNone(matched)
        self.assertEqual(5, len(matched))
        self.assertTrue([['?x', 'MONKEY'], ['?y', 'LEGS'], ['?z', '2']] in matched)
        self.assertTrue([['?x', 'MONKEY'], ['?y', 'HASFUR'], ['?z', 'true']] in matched)
        self.assertTrue([['?x', 'ELEPHANT'], ['?y', 'TRUNK'], ['?z', 'true']] in matched)
        self.assertTrue([['?x', 'ZEBRA'], ['?y', 'LEGS'], ['?z', '4']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['?y', 'LEGS'], ['?z', '2']] in matched)

    def test_not_match_vars_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars("?x", "?y", "?z")
        self.assertIsNotNone(matched)
        self.assertEqual(0, len(matched))

    def test_match_vars_subject_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="?x",obj="?z")
        self.assertIsNotNone(matched)
        self.assertEqual(5, len(matched))
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'LEGS'], ['?z', '2']] in matched)
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'HASFUR'], ['?z', 'true']] in matched)
        self.assertTrue([['?x', 'ELEPHANT'], ['pred', 'TRUNK'], ['?z', 'true']] in matched)
        self.assertTrue([['?x', 'ZEBRA'], ['pred', 'LEGS'], ['?z', '4']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['pred', 'LEGS'], ['?z', '2']] in matched)

    def test_match_vars_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(predicate="?x")
        self.assertIsNotNone(matched)
        self.assertTrue([['subj', 'MONKEY'], ['?x', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['?x', 'HASFUR'], ['obj', 'true']] in matched)
        self.assertTrue([['subj', 'ELEPHANT'], ['?x', 'TRUNK'], ['obj', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['?x', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['?x', 'LEGS'], ['obj', '2']] in matched)

    def test_match_vars_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(predicate="?x", obj="?y")
        self.assertIsNotNone(matched)
        self.assertTrue([['subj', 'MONKEY'], ['?x', 'LEGS'], ['?y', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['?x', 'HASFUR'], ['?y', 'true']] in matched)
        self.assertTrue([['subj', 'ELEPHANT'], ['?x', 'TRUNK'], ['?y', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['?x', 'LEGS'], ['?y', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['?x', 'LEGS'], ['?y', '2']] in matched)

    def test_match_vars_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(obj="?x")
        self.assertIsNotNone(matched)
        self.assertEqual(5, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'LEGS'], ['?x', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'HASFUR'], ['?x', 'true']] in matched)
        self.assertTrue([['subj', 'ELEPHANT'], ['pred', 'TRUNK'], ['?x', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['pred', 'LEGS'], ['?x', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['pred', 'LEGS'], ['?x', '2']] in matched)

    def test_match_vars_object_with_subject_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="MONKEY", obj="?x")
        self.assertIsNotNone(matched)
        self.assertEqual(2, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'LEGS'], ['?x', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'HASFUR'], ['?x', 'true']] in matched)

    def test_not_match_vars_object_with_subject_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="MONKEY", obj="?x")
        self.assertIsNotNone(matched)
        self.assertEqual(3, len(matched))
        self.assertTrue([['subj', 'ELEPHANT'], ['pred', 'TRUNK'], ['?x', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['pred', 'LEGS'], ['?x', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['pred', 'LEGS'], ['?x', '2']] in matched)

    def test_match_vars_object_with_subject_predicate_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="MONKEY", predicate="LEGS", obj="?x")
        self.assertIsNotNone(matched)
        self.assertEqual(1, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'LEGS'], ['?x', '2']] in matched)

    def test_not_match_vars_object_with_subject_predicate_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="MONKEY", predicate="LEGS", obj="?x")
        self.assertIsNotNone(matched)
        self.assertEqual(3, len(matched))
        self.assertTrue([['subj', 'ELEPHANT'], ['pred', 'TRUNK'], ['?x', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['pred', 'LEGS'], ['?x', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['pred', 'LEGS'], ['?x', '2']] in matched)

    def match_only_vars(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_only_vars(subject="MONKEY", obj="?x")
        self.assertIsNotNone(matched)
        self.assertEqual(2, len(matched))
        self.assertTrue([['?x', '2']] in matched)
        self.assertTrue([['?x', 'true']] in matched)

    def test_chungyilinxrspace_issue_175(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACTOR", "ISA", "PERSON", "TEST")
        collection.add_entity("ACTOR", "ISA", "MAN", "TEST")

        set1 = collection.match_to_vars("ACTOR", "ISA", "?x")

        self.assertTrue([['subj', 'ACTOR'], ['pred', 'ISA'], ['?x', 'MAN']] in set1)
        self.assertTrue([['subj', 'ACTOR'], ['pred', 'ISA'], ['?x', 'PERSON']] in set1)
