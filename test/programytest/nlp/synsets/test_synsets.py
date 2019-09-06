import unittest

from programy.nlp.synsets.synsets import Synsets


class SynsetsTests(unittest.TestCase):

    def test_get_similar_words(self):
        self.assertEquals(['hack', 'machine_politician', 'cab', 'chop'], Synsets.get_similar_words("hack"))
        self.assertEquals([], Synsets.get_similar_words(""))
        self.assertEquals([], Synsets.get_similar_words("lkjghjokg"))

    def test_get_similar_words_weighted(self):
        self.assertEquals(['hack', 'cab', 'chop'], Synsets.get_similar_words("hack", weight=3))
        self.assertEquals([], Synsets.get_similar_words("hack", weight=10))

    def test_get_similar_verbs(self):
        self.assertEquals(['travel', 'go', 'become', 'run', 'proceed', 'sound', 'function', 'run_low', 'move',
                           'survive', 'die', 'belong', 'start', 'blend', 'fit', 'rifle', 'plump', 'fail'],
                          Synsets.get_similar_verbs("going"))
        self.assertEquals([], Synsets.get_similar_verbs(""))
        self.assertEquals([], Synsets.get_similar_verbs("lkjghjokg"))

    def test_get_similar_nouns(self):
        self.assertEquals(['cat', 'guy', 'kat', "cat-o'-nine-tails",
                           'caterpillar', 'big_cat', 'computerized_tomography'],
                          Synsets.get_similar_nouns("cat"))
        self.assertEquals([], Synsets.get_similar_nouns(""))
        self.assertEquals([], Synsets.get_similar_nouns("lkjghjokg"))

    def test_get_similar_adjectives(self):
        self.assertEquals(['red', 'crimson'], Synsets.get_similar_adjectives("red"))
        self.assertEquals([], Synsets.get_similar_adjectives(""))
        self.assertEquals([], Synsets.get_similar_adjectives("lkjghjokg"))

    def test_get_similar_adverbs(self):
        self.assertEquals(['gently', 'lightly'], Synsets.get_similar_adverbs("gently"))
        self.assertEquals([], Synsets.get_similar_adverbs(""))
        self.assertEquals([], Synsets.get_similar_adverbs("lkjghjokg"))

    def test_get_similarity(self):
        self.assertEquals([('octopus', 'runt', 0.1),
                           ('octopus', 'prawn', 0.3333333333333333),
                           ('octopus', 'shrimp', 0.0625),
                           ('octopus', 'runt', 0.1),
                           ('octopus', 'prawn', 0.0625),
                           ('octopus', 'shrimp', 0.1111111111111111)],
                          Synsets.get_similarity("Octopus", "Shrimp"))
