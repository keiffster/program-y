import unittest

from programy.config.file.factory import ConfigurationFactory
from programy.clients.events.console.config import ConsoleConfiguration


class ConfigurationFactoryTests(unittest.TestCase):

    def test_guess_format_from_filename(self):
        config_format = ConfigurationFactory.guess_format_from_filename("file.yaml")
        self.assertEqual(config_format, "yaml")
        config_format = ConfigurationFactory.guess_format_from_filename("file.json")
        self.assertEqual(config_format, "json")
        config_format = ConfigurationFactory.guess_format_from_filename("file.xml")
        self.assertEqual(config_format, "xml")

    def test_guess_format_no_extension(self):
        with self.assertRaises(Exception):
            ConfigurationFactory.guess_format_from_filename("file_yaml")

    def test_get_config_by_name(self):
        config_type = ConfigurationFactory.get_config_by_name("yaml")
        self.assertIsNotNone(config_type)
        config_type = ConfigurationFactory.get_config_by_name("json")
        self.assertIsNotNone(config_type)
        config_type = ConfigurationFactory.get_config_by_name("xml")
        self.assertIsNotNone(config_type)

    def test_get_config_by_name_wrong_extension(self):
        with self.assertRaises(Exception):
            ConfigurationFactory.get_config_by_name("other")
        with self.assertRaises(Exception):
            ConfigurationFactory.get_config_by_name("")
        with self.assertRaises(Exception):
            ConfigurationFactory.get_config_by_name(None)

    def test_load_configuration_from_file(self):
        with self.assertRaises(Exception):
            ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(), "file.txt", file_format=None)
        with self.assertRaises(Exception):
            ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(), "file.txt", file_format="")
