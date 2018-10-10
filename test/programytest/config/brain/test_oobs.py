import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.oobs import BrainOOBSConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainOOBsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oob:
              default:
                classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
              dial:
                classname: programy.oob.defaults.dial.DialOutOfBandProcessor
              email:
                classname: programy.oob.defaults.email.EmailOutOfBandProcessor
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
