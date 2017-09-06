import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.oobs import BrainOOBSConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainOOBsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oob:
              default:
                classname: programy.utils.oob.default.DefaultOutOfBandProcessor
              dial:
                classname: programy.utils.oob.dial.DialOutOfBandProcessor
              email:
                classname: programy.utils.oob.email.EmailOutOfBandProcessor
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(oobs_config.exists("default"))
        self.assertTrue(oobs_config.exists("dial"))
        self.assertTrue(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oobs:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(oobs_config.exists("default"))
        self.assertFalse(oobs_config.exists("dial"))
        self.assertFalse(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(oobs_config.exists("default"))
        self.assertFalse(oobs_config.exists("dial"))
        self.assertFalse(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))
