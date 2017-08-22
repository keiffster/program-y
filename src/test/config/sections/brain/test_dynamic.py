import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.dynamic import BrainDynamicsConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainDynamicsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
                variables:
                    gettime: programy.dynamic.variables.datetime.GetTime
                sets:
                    number: programy.dynamic.sets.numeric.IsNumeric
                    roman:   programy.dynamic.sets.roman.IsRomanNumeral
                maps:
                    romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
                    dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")


    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")


    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamic_config = BrainDynamicsConfiguration()
        dynamic_config.load_config_section(yaml, brain_config, ".")


