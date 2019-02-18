import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.oob import BrainOOBConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainOOBConfigurationTests(unittest.TestCase):

    def test_oob_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oobs:
              default:
                classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        oobs_config = yaml.get_section("oobs", brain_config)
        self.assertIsNotNone(oobs_config)

        oob_config = BrainOOBConfiguration("default")
        oob_config.load_config_section(yaml, oobs_config, ".")

        self.assertEqual("programy.oob.defaults.default.DefaultOutOfBandProcessor", oob_config.classname)

    def test_default_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oobs:
                default:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        oobs_config = yaml.get_section("oobs", brain_config)
        self.assertIsNotNone(oobs_config)

        oob_config = BrainOOBConfiguration("default")
        oob_config.load_config_section(yaml, oobs_config, ".")

        self.assertIsNone(oob_config.classname)


