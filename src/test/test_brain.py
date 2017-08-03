import unittest
import os
import xml.etree.ElementTree as ET

from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.console import ConsoleConfiguration
from programy.utils.security.authorise.authorisor import AuthorisationException
from programy.utils.oob.default import DefaultOutOfBandProcessor
from programy.utils.oob.dial import DialOutOfBandProcessor
from programy.utils.oob.email import EmailOutOfBandProcessor

class BrainTests(unittest.TestCase):

    def load_os_specific_configuration(self, yaml, linux_filename, windows_filename):
        if os.name == 'posix':
            yaml.load_from_file(os.path.dirname(__file__)+ os.sep + linux_filename, ConsoleConfiguration(), os.path.dirname(__file__))
        elif os.name == 'nt':
            yaml.load_from_file(os.path.dirname(__file__)+ os.sep + windows_filename, ConsoleConfiguration(), os.path.dirname(__file__))
        else:
            raise Exception("Unknown os [%s]"%os.name)

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
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

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

        oob_content = ET.fromstring("<oob><something>other</something></oob>")
        self.assertEqual("<?xml version='1.0' encoding='utf8'?>\n<oob><something>other</something></oob>", brain.default_oob.process_out_of_bounds(None, "console", oob_content))
        oob_content = ET.fromstring("<oob><dial>07777777777</dial></oob>")
        self.assertEqual("", brain.oobs['dial'].process_out_of_bounds(None, "console", oob_content))

    def test_brain_init_with_secure_config(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_secure_brain.yaml", "test_secure_brain.windows.yaml")

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
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        brain = Brain(brain_config)

        self.assertIsInstance(brain.default_oob, DefaultOutOfBandProcessor)
        self.assertIsInstance(brain.oobs['dial'], DialOutOfBandProcessor)
        self.assertIsInstance(brain.oobs['email'], EmailOutOfBandProcessor)

    def test_oob_stripping(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

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
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        brain = Brain(brain_config)

        self.assertEqual("", brain.process_oob(None, "console", "<oob></oob>"))
