import unittest

from programy.config.file.file import BaseConfigurationFile
from programy.utils.substitutions.substitues import Substitutions


class TestBaseConfigurationFile(BaseConfigurationFile):

    def load_from_text(self, text, client_configuration, bot_root):
        return None

    def load_from_file(self, filename, client_configuration, bot_root):
        return None

    def get_section(self, section_name, parent_section=None):
        return None

    def get_section_data(self, section_name, parent_section=None):
        return None

    def get_child_section_keys(self, section_name, parent_section=None):
        return None

    def get_option(self, section, option_name, missing_value=None, subs: Substitutions = None):
        return None


class BaseConfigurationFileTests(unittest.TestCase):

    def test_convert_to_bool(self):
        config = TestBaseConfigurationFile()

        self.assertTrue(config.convert_to_bool("true"))
        self.assertTrue(config.convert_to_bool("True"))
        self.assertTrue(config.convert_to_bool("TRUE"))

        self.assertFalse(config.convert_to_bool("false"))
        self.assertFalse(config.convert_to_bool("False"))
        self.assertFalse(config.convert_to_bool("FALSE"))

        with self.assertRaises(Exception):
            config.convert_to_bool("")

        with self.assertRaises(Exception):
            config.convert_to_bool("XXX")

    def test_convert_to_int(self):
        config = TestBaseConfigurationFile()

        self.assertEqual(0, config.convert_to_int('0'))
        self.assertEqual(10, config.convert_to_int('10'))

        with self.assertRaises(Exception):
            config.convert_to_int("")

        with self.assertRaises(Exception):
            config.convert_to_int("XXX")
