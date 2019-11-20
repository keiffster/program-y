import unittest

from programy.nlp.synsets.synsets import Synsets


class SynsetsTests(unittest.TestCase):

    def test_get_similar_words(self):
        synsets = Synsets()
        self.assertIsNotNone(synsets)
        
        self.assertEqual(['hack', 'machine_politician', 'cab', 'chop'], synsets.get_similar_words("hack"))
        self.assertEqual([], synsets.get_similar_words(""))
        self.assertEqual([], synsets.get_similar_words("lkjghjokg"))

    def test_get_similar_words_weighted(self):
        synsets = Synsets()
        self.assertIsNotNone(synsets)

        self.assertEqual(['hack', 'cab', 'chop'], synsets.get_similar_words("hack", weight=3))
        self.assertEqual([], synsets.get_similar_words("hack", weight=10))

    def test_get_similar_verbs(self):
        synsets = Synsets()
        self.assertIsNotNone(synsets)

        self.assertEqual(['travel', 'go', 'become', 'run', 'proceed', 'sound', 'function', 'run_low', 'move',
                           'survive', 'die', 'belong', 'start', 'blend', 'fit', 'rifle', 'plump', 'fail'],
                          synsets.get_similar_verbs("going"))
        self.assertEqual([], synsets.get_similar_verbs(""))
        self.assertEqual([], synsets.get_similar_verbs("lkjghjokg"))

    def test_get_similar_nouns(self):
        synsets = Synsets()
        self.assertIsNotNone(synsets)

        self.assertEqual(['cat', 'guy', 'kat', "cat-o'-nine-tails",
                           'caterpillar', 'big_cat', 'computerized_tomography'],
                          synsets.get_similar_nouns("cat"))
        self.assertEqual([], synsets.get_similar_nouns(""))
        self.assertEqual([], synsets.get_similar_nouns("lkjghjokg"))

    def test_get_similar_adjectives(self):
        synsets = Synsets()
        self.assertIsNotNone(synsets)

        self.assertEqual(['red', 'crimson'], synsets.get_similar_adjectives("red"))
        self.assertEqual([], synsets.get_similar_adjectives(""))
        self.assertEqual([], synsets.get_similar_adjectives("lkjghjokg"))

    def test_get_similar_adverbs(self):
        synsets = Synsets()
        self.assertIsNotNone(synsets)

        self.assertEqual(['gently', 'lightly'], synsets.get_similar_adverbs("gently"))
        self.assertEqual([], synsets.get_similar_adverbs(""))
        self.assertEqual([], synsets.get_similar_adverbs("lkjghjokg"))

    def test_get_similarity(self):
        synsets = Synsets()
        self.assertIsNotNone(synsets)

        self.assertEqual([('octopus', 'runt', 0.1),
                           ('octopus', 'prawn', 0.3333333333333333),
                           ('octopus', 'shrimp', 0.0625),
                           ('octopus', 'runt', 0.1),
                           ('octopus', 'prawn', 0.0625),
                           ('octopus', 'shrimp', 0.1111111111111111)],
                          synsets.get_similarity("Octopus", "Shrimp"))
