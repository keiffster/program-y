import unittest

from programy.rdf.collection import RDFCollection


class RDFCollectionTests(unittest.TestCase):

    def add_data(self, collection):
        collection.add_entity("MONKEY", "LEGS", "2")
        collection.add_entity("MONKEY", "HASFUR", "true")
        collection.add_entity("ZEBRA", "LEGS", "4")
        collection.add_entity("BIRD", "LEGS", "2")
        collection.add_entity("ELEPHANT", "TRUNK", "true")

    ###################################################################################################################
    # RDF Database creation
    #

    def test_collection(self):
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
        self.assertTrue(collection.has_object('ACCOUNT', 'ISA', 'Concept'))

        self.assertFalse(collection.has_subject('ACCOUNTX'))
        self.assertFalse(collection.has_predicate('ACCOUNT', 'hasSizeX'))
        self.assertFalse(collection.has_object('ACCOUNT', 'isa', 'ConceptX'))

    def test_add_collection(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    def test_delete_collection_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT")

        self.assertFalse(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize")

        self.assertFalse(collection.has_subject('ACCOUNT'))

    def test_delete_collection_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("ACCOUNT", "hasSize", "0")
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

        collection.add_entity("ACCOUNT", "hasSize", "0")
        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

        collection.delete_entity("ACCOUNT", "hasSize", "1")

        self.assertTrue(collection.has_subject('ACCOUNT'))
        self.assertTrue(collection.has_predicate('ACCOUNT', 'hasSize'))
        self.assertTrue(collection.has_object('ACCOUNT', 'hasSize', "0"))

    ###################################################################################################################
    # Basic matching
    #

    def test_all_as_tuples(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()
        self.assertIsNotNone(all)
        self.assertEquals(5, len(all))
        self.assertTrue(["MONKEY", "LEGS", "2"] in all)
        self.assertTrue(["MONKEY", "HASFUR", "true"] in all)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in all)
        self.assertTrue(["BIRD", "LEGS", "2"] in all)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in all)

    def test_match_all_as_tuples(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples()
        self.assertIsNotNone(matched)
        self.assertEquals(5, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["MONKEY", "HASFUR", "true"] in matched)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in matched)
        self.assertTrue(["BIRD", "LEGS", "2"] in matched)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in matched)

    def test_match_all_as_tuples_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY")
        self.assertIsNotNone(matched)
        self.assertEquals(2, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["MONKEY", "HASFUR", "true"] in matched)

    def test_match_all_as_tuples_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY", predicate="LEGS")
        self.assertIsNotNone(matched)
        self.assertEquals(1, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)

    def test_match_all_as_tuples_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY", predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEquals(1, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)

    def test_match_all_as_tuples_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(predicate="LEGS")
        self.assertIsNotNone(matched)
        self.assertEquals(3, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in matched)
        self.assertTrue(["BIRD", "LEGS", "2"] in matched)

    def test_match_all_as_tuples_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEquals(2, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["BIRD", "LEGS", "2"] in matched)

    def test_match_as_tuples_subject_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY", obj="2")
        self.assertIsNotNone(matched)
        self.assertEquals(1, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)

    def test_remove_subject(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY')
        self.assertIsNotNone(remains)
        self.assertEquals(3, len(remains))
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
        self.assertEquals(4, len(remains))
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
        self.assertEquals(4, len(remains))
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
        self.assertEquals(2, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)

    def test_remove_predicate_object(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, predicate='LEGS', obj="2")
        self.assertIsNotNone(remains)
        self.assertEquals(3, len(remains))
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
        self.assertEquals(3, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "true"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "true"] in remains)

    ###################################################################################################################
    # Vars matching
    #

    def test_match_vars(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars()
        self.assertIsNotNone(matched)
        self.assertEquals(5, len(matched))
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
        self.assertEquals(0, len(matched))

    def test_match_vars_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars("?x")
        self.assertIsNotNone(matched)
        self.assertEquals(5, len(matched))
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
        self.assertEquals(0, len(not_matched))

    def test_match_vars_subject_with_predicate_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="?x", predicate="LEGS")
        self.assertIsNotNone(matched)
        self.assertEquals(3, len(matched))
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['?x', 'ZEBRA'], ['pred', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars_subject_with_predicate_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        not_matched = collection.not_match_to_vars(subject="?x", predicate="LEGS")
        self.assertIsNotNone(not_matched)
        self.assertEquals(1, len(not_matched))
        self.assertTrue([['?x', 'ELEPHANT'], ['pred', 'TRUNK'], ['obj', 'true']] in not_matched)

    def test_match_vars_subject_with_predicate_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="?x", predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEquals(2, len(matched))
        self.assertTrue([['?x', 'MONKEY'], ['pred', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['?x', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars_subject_with_predicate_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="?x", predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEquals(2, len(matched))
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
        self.assertEquals(2, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['?y', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['?y', 'HASFUR'], ['obj', 'true']] in matched)

    def test_not_match_vars_subject_predicate_with_subject_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="MONKEY", predicate="?y")
        self.assertIsNotNone(matched)
        self.assertEquals(3, len(matched))
        self.assertTrue([['subj', 'ZEBRA'], ['?y', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['?y', 'LEGS'], ['obj', '2']] in matched)
        self.assertTrue([['subj', 'ELEPHANT'], ['?y', 'TRUNK'], ['obj', 'true']] in matched)

    def test_match_vars_subject_predicate_with_subject_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="MONKEY", predicate="?y", obj="2")
        self.assertIsNotNone(matched)
        self.assertEquals(1, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['?y', 'LEGS'], ['obj', '2']] in matched)

    def test_not_match_vars_subject_predicate_with_subject_object_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="MONKEY", predicate="?y", obj="2")
        self.assertIsNotNone(matched)
        self.assertEquals(3, len(matched))
        self.assertTrue([['subj', 'ELEPHANT'], ['?y', 'TRUNK'], ['obj', 'true']] in matched)
        self.assertTrue([['subj', 'ZEBRA'], ['?y', 'LEGS'], ['obj', '4']] in matched)
        self.assertTrue([['subj', 'BIRD'], ['?y', 'LEGS'], ['obj', '2']] in matched)

    def test_match_vars_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars("?x", "?y", "?z")
        self.assertIsNotNone(matched)
        self.assertEquals(5, len(matched))
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
        self.assertEquals(0, len(matched))

    def test_match_vars_subject_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.match_to_vars(subject="?x",obj="?z")
        self.assertIsNotNone(matched)
        self.assertEquals(5, len(matched))
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
        self.assertEquals(5, len(matched))
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
        self.assertEquals(2, len(matched))
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'LEGS'], ['?x', '2']] in matched)
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'HASFUR'], ['?x', 'true']] in matched)

    def test_not_match_vars_object_with_subject_params(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.not_match_to_vars(subject="MONKEY", obj="?x")
        self.assertIsNotNone(matched)
        self.assertEquals(3, len(matched))
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
        self.assertEquals(2, len(matched))
        self.assertTrue([['?x', '2']] in matched)
        self.assertTrue([['?x', 'true']] in matched)

    ###################################################################################################################
    # Vars unification
    #

    def test_unify_on_single_var(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("MONKEY", "LEGS", "2")
        collection.add_entity("MONKEY", "HASFUR", "true")
        collection.add_entity("ZEBRA", "LEGS", "4")
        collection.add_entity("BIRD", "LEGS", "2")
        collection.add_entity("ELEPHANT", "TRUNK", "true")

        set1 = collection.match_to_vars("?x", "LEGS", "2")
        set2 = collection.match_to_vars("?x", "HASFUR", "true")

        unified = collection.unify(["?x"], [set1, set2])
        self.assertIsNotNone(unified)
        self.assertEquals(1, len(unified))
        self.assertTrue([['?x', 'MONKEY']] in unified)

    def test_unify_on_single_var_with_not(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("MONKEY", "LEGS", "2")
        collection.add_entity("MONKEY", "HASFUR", "true")
        collection.add_entity("ZEBRA", "LEGS", "4")
        collection.add_entity("BIRD", "LEGS", "2")
        collection.add_entity("ELEPHANT", "TRUNK", "true")

        set1 = collection.match_to_vars("?x", "LEGS", "2")
        set2 = collection.not_match_to_vars("?x", "HASFUR", "true")

        unified = collection.unify(["?x"], [set1, set2])
        self.assertIsNotNone(unified)
        self.assertEquals(1, len(unified))
        self.assertTrue([['?x', 'BIRD']] in unified)

    def test_unify_on_multi_vars(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("TEST1", "ISA", "TEST2")
        collection.add_entity("TEST2", "ISA", "TEST3")

        set1 = collection.match_to_vars("?x", "ISA", "?y")
        set2 = collection.match_to_vars("?y", "ISA", "?z")

        unified = collection.unify(("?x", "?y", "?z"), [set1, set2])
        self.assertIsNotNone(unified)
        self.assertEquals(1, len(unified))
        self.assertTrue(["?x", "TEST1"] in unified[0])
        self.assertTrue(["?y", "TEST2"] in unified[0])
        self.assertTrue(["?z", "TEST3"] in unified[0])

    def test_unify_multi_var_deep(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("TEST1", "ISA", "TEST2")
        collection.add_entity("TEST2", "ISA", "TEST3")
        collection.add_entity("TEST3", "ISA", "TEST4")
        collection.add_entity("TEST4", "ISA", "TEST5")

        set1 = collection.match_to_vars("?x", "ISA", "?y")
        set2 = collection.match_to_vars("?y", "ISA", "?z")
        set3 = collection.match_to_vars("?z", "ISA", "?w")

        unified = collection.unify(("?x", "?y", "?z", "?w"), [set1, set2, set3])
        self.assertIsNotNone(unified)
        self.assertEquals(2, len(unified))
        self.assertTrue([['?x', 'TEST1'], ['?y', 'TEST2'], ['?z', 'TEST3'], ['?w', 'TEST4'], ] in unified)
        self.assertTrue([['?x', 'TEST2'], ['?y', 'TEST3'], ['?z', 'TEST4'], ['?w', 'TEST5']] in unified)

