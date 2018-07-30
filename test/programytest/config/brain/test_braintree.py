import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.braintree import BrainBraintreeConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainBraintreeConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            braintree:
              create: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        braintree_config = BrainBraintreeConfiguration()
        braintree_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue("file", braintree_config.create)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            braintree:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        braintree_config = BrainBraintreeConfiguration()
        braintree_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(braintree_config.create)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        braintree_config = BrainBraintreeConfiguration()
        braintree_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(braintree_config.create)
