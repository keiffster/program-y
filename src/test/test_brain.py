import unittest
import os

from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.console import ConsoleConfiguration

class BrainTests(unittest.TestCase):

    def test_brain_init_no_config(self):
        brain = Brain(BrainConfiguration() )
        self.assertIsNotNone(brain)

        self.assertIsNotNone(brain.aiml_parser)
        self.assertIsNotNone(brain.denormals)
        self.assertIsNotNone(brain.normals)
        self.assertIsNotNone(brain.genders)
        self.assertIsNotNone(brain.persons)
        self.assertIsNotNone(brain.person2s)
        self.assertIsNotNone(brain.predicates)
        self.assertIsNotNone(brain.pronouns)
        self.assertIsNotNone(brain.properties)
        self.assertIsNotNone(brain.triples)
        self.assertIsNotNone(brain.sets)
        self.assertIsNotNone(brain.maps)
        self.assertIsNotNone(brain.preprocessors)
        self.assertIsNotNone(brain.postprocessors)

    def test_brain_init_with_config(self):

        yaml = YamlConfigurationFile()
        yaml.load_from_file(os.path.dirname(__file__)+"/test_brain.yaml", ConsoleConfiguration(), ".")

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        brain = Brain(brain_config)
        self.assertIsNotNone(brain)

        self.assertIsNotNone(brain.aiml_parser)
        self.assertIsNotNone(brain.denormals)
        self.assertIsNotNone(brain.normals)
        self.assertIsNotNone(brain.genders)
        self.assertIsNotNone(brain.persons)
        self.assertIsNotNone(brain.person2s)
        self.assertIsNotNone(brain.predicates)
        self.assertIsNotNone(brain.pronouns)
        self.assertIsNotNone(brain.properties)
        self.assertIsNotNone(brain.triples)
        self.assertIsNotNone(brain.sets)
        self.assertIsNotNone(brain.maps)
        self.assertIsNotNone(brain.preprocessors)
        self.assertIsNotNone(brain.postprocessors)

        if os.path.exists(brain_config.binaries.binary_filename):
            os.remove(brain_config.binaries.binary_filename)
        self.assertFalse(os.path.exists(brain_config.binaries.binary_filename))
        brain.save_binary(brain_config)
        self.assertTrue(os.path.exists(brain_config.binaries.binary_filename))
        brain.load_binary(brain_config)
