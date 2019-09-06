import unittest

from programy.nlp.wordnet.wordnet import WordNet


class WordNetTests(unittest.TestCase):

    def test_get_definitions(self):

        self.assertEquals(['tentacles of octopus prepared as food',
                           'bottom-living cephalopod having a soft oval body with eight long tentacles'],
                          WordNet.get_definitions("octopus"))

        self.assertEquals(['tentacles of octopus prepared as food',
                           'bottom-living cephalopod having a soft oval body with eight long tentacles'],
                          WordNet.get_definitions("octopi"))

        self.assertEquals([],
                          WordNet.get_definitions(""))
