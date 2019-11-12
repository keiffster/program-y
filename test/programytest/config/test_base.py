import os
import unittest

from programy.config.base import BaseConfigurationData
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.license.keys import LicenseKeys


class MockBaseConfigurationData(BaseConfigurationData):

    def __init__(self, name):
        BaseConfigurationData.__init__(self, name)

    def load_config_section(self, configuration_file, configuration, bot_root, subs = None):
        service = configuration_file.get_section(self.section_name, configuration)
        if service is not None:
            self.load_additional_key_values(configuration_file, service)

    def additionals_to_add(self):
        return ["val1", "val2"]


class BaseConfigurationDataTests(unittest.TestCase):

    def test_sub_bot_root(self):
        config = BaseConfigurationData("test")

        replaced = config.sub_bot_root( os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "data")

        replaced = config.sub_bot_root("$BOT_ROOT"+ os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "root" + os.sep + "data")

        replaced = config.sub_bot_root("$BOT_ROOT$BOT_ROOT"+ os.sep + "data",  os.sep + "root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced,  os.sep + "root" + os.sep + "root" + os.sep + "data")

    def test_additionals(self):
        config = BaseConfigurationData("test")

        self.assertEqual([], config.additionals_to_add())

        config._additionals["key1"] = "value1"
        config._additionals["key2"] = "value2"

        self.assertTrue(config.exists("key1"))
        self.assertEqual("value1", config.value("key1"))

        self.assertTrue(config.exists("key2"))
        self.assertEqual("value2", config.value("key2"))

        self.assertFalse(config.exists("key3"))

    def test_extract_license_key(self):
        config = BaseConfigurationData("test")

        license_keys = LicenseKeys()
        license_keys.add_key("key", "value")

        self.assertEqual("value", config._extract_license_key("LICENSE:key", license_keys))

    def test_extract_license_key_null_attr(self):
        config = BaseConfigurationData("test")

        license_keys = LicenseKeys()
        license_keys.add_key("key", "value")

        self.assertEqual(None, config._extract_license_key(None, license_keys))

    def test_extract_license_key_diff_key(self):
        config = BaseConfigurationData("test")

        license_keys = LicenseKeys()
        license_keys.add_key("key", "value")

        self.assertEqual("keyX", config._extract_license_key("keyX", license_keys))

    def test_extract_license_key_diff_key2(self):
        config = BaseConfigurationData("test")

        license_keys = LicenseKeys()
        license_keys.add_key("key", "value")

        self.assertEqual(None, config._extract_license_key("LICENSE:keyX", license_keys))

    def test_load_additional_key_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        base:
            test:
                val1: test3
                val2: test4
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("base")

        base_config = MockBaseConfigurationData("test")

        base_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals("test3", base_config._additionals["val1"])