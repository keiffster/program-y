import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.braintree import BrainBraintreeConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


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

    def test_defaults(self):
        braintree_config = BrainBraintreeConfiguration()
        data = {}
        braintree_config.to_yaml(data, True)

        BrainBraintreeConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertFalse(data['create'])
        test.assertEqual(data['save_as_user'], "system")
