import unittest

from programy.brain import Brain
from programy.config.brain import BrainConfiguration

class BrainTests(unittest.TestCase):

    def test_brain_init(self):
        brain = Brain(BrainConfiguration() )
        self.assertIsNotNone(brain)

        self.assertIsNotNone(brain._aiml_parser)
        self.assertIsNotNone(brain._denormal_collection)
        self.assertIsNotNone(brain._normal_collection)
        self.assertIsNotNone(brain._gender_collection)
        self.assertIsNotNone(brain._person_collection)
        self.assertIsNotNone(brain._person2_collection)
        self.assertIsNotNone(brain._predicates_collection)
        self.assertIsNotNone(brain._pronouns_collection)
        self.assertIsNotNone(brain._properties_collection)
        self.assertIsNotNone(brain._triples_collection)
        self.assertIsNotNone(brain._sets_collection)
        self.assertIsNotNone(brain._maps_collection)
        self.assertIsNotNone(brain._preprocessors)
        self.assertIsNotNone(brain._postprocessors)
