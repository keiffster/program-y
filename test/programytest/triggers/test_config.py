import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.triggers.config import TriggerConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class TriggersConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            triggers:
                manager: programy.triggers.rest.RestTriggerManager
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.rest.RestTriggerManager", triggers_config.manager)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            triggers:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.local.LocalTriggerManager", triggers_config.manager)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.local.LocalTriggerManager", triggers_config.manager)

    def test_with_additional_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            triggers:
                manager: programy.triggers.rest.RestTriggerManager
                host: localhost
                port: 8080
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEquals("programy.triggers.rest.RestTriggerManager", triggers_config.manager)
        self.assertEquals("localhost", triggers_config.value("host"))
        self.assertEquals(8080, triggers_config.value("port"))
