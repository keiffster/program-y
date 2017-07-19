import unittest
import os

from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.console import ConsoleConfiguration
from programy.utils.security.authorise.authorisor import AuthorisationException
from programy.utils.oob.default import DefaultOutOfBoundsProcessor
from programy.utils.oob.dial import DialOutOfBoundsProcessor
from programy.utils.oob.email import EmailOutOfBoundsProcessor

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
        self.assertIsNone(brain.default_oob)
        self.assertIsNotNone(brain.oobs)

    def test_brain_init_with_config(self):

        yaml = YamlConfigurationFile()
        yaml.load_from_file(os.path.dirname(__file__)+"/test_brain.yaml", ConsoleConfiguration(), os.path.dirname(__file__))

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
        self.assertIsNotNone(brain.authentication)
        self.assertIsNotNone(brain.authorisation)
        self.assertIsNotNone(brain.default_oob)
        self.assertIsNotNone(brain.oobs)

        if os.path.exists(brain_config.binaries.binary_filename):
            os.remove(brain_config.binaries.binary_filename)
        self.assertFalse(os.path.exists(brain_config.binaries.binary_filename))
        brain.save_binary(brain_config)
        self.assertTrue(os.path.exists(brain_config.binaries.binary_filename))
        brain.load_binary(brain_config)

        self.assertTrue(brain.authentication.authenticate("console"))
        self.assertTrue(brain.authentication.authenticate("someone"))

        self.assertTrue(brain.authorisation.authorise("console", "somthing"))
        self.assertTrue(brain.authorisation.authorise("someone", "other"))

        self.assertEqual("<something>other</something>", brain.default_oob.process_out_of_bounds(None, "console", "<something>other</something>"))
        self.assertEqual("", brain.oobs['dial'].process_out_of_bounds(None, "console", "<dial>07777777777</dial>"))

    def test_brain_init_with_secure_config(self):

        yaml = YamlConfigurationFile()
        yaml.load_from_file(os.path.dirname(__file__)+ os.sep + "test_secure_brain.yaml", ConsoleConfiguration(), os.path.dirname(__file__))

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, os.path.dirname(__file__))

        brain = Brain(brain_config)
        self.assertIsNotNone(brain)

        self.assertTrue(brain.authentication.authenticate("console"))
        self.assertFalse(brain.authentication.authenticate("someone"))

        self.assertTrue(brain.authorisation.authorise("console", "root"))
        self.assertFalse(brain.authorisation.authorise("console", "unknown"))
        with self.assertRaises(AuthorisationException):
            brain.authorisation.authorise("someone", "root")

    def test_oob_loading(self):

        yaml = YamlConfigurationFile()
        yaml.load_from_file(os.path.dirname(__file__)+"/test_brain.yaml", ConsoleConfiguration(), os.path.dirname(__file__))

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        brain = Brain(brain_config)

        self.assertIsInstance(brain.default_oob, DefaultOutOfBoundsProcessor)
        self.assertIsInstance(brain.oobs['dial'], DialOutOfBoundsProcessor)
        self.assertIsInstance(brain.oobs['email'], EmailOutOfBoundsProcessor)

    def test_oob_stripping(self):

        yaml = YamlConfigurationFile()
        yaml.load_from_file(os.path.dirname(__file__)+"/test_brain.yaml", ConsoleConfiguration(), os.path.dirname(__file__))

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        brain = Brain(brain_config)

        response, oob = brain.strip_oob("<oob>command</oob>")
        self.assertEqual("", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob>")
        self.assertEqual("This ", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob> That")
        self.assertEqual("This That", response)
        self.assertEqual("<oob>command</oob>", oob)

    def test_oob_processing(self):

        yaml = YamlConfigurationFile()
        yaml.load_from_file(os.path.dirname(__file__)+"/test_brain.yaml", ConsoleConfiguration(), os.path.dirname(__file__))

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        brain = Brain(brain_config)

        self.assertEqual("", brain.process_oob(None, "console", ""))
