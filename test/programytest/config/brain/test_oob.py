import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.oob import BrainOOBConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


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

    def test_to_yaml_defaults(self):
        oob_config = BrainOOBConfiguration("default")

        data = {}
        oob_config.to_yaml(data, defaults=True)
        self.assertEquals({'classname': 'programy.oob.defaults.default.DefaultOutOfBandProcessor'}, data)

    def test_to_yaml_no_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oobs:
              default:
                classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        oobs_config = yaml.get_section("oobs", brain_config)

        oob_config = BrainOOBConfiguration("default")
        oob_config.load_config_section(yaml, oobs_config, ".")

        data = {}
        oob_config.to_yaml(data, defaults=False)
        self.assertEquals({'classname': 'programy.oob.defaults.default.DefaultOutOfBandProcessor'}, data)
