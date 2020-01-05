import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.triggers.config import TriggerConfiguration


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

        self.assertEqual("programy.triggers.rest.RestTriggerManager", triggers_config.manager)

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

        self.assertEqual("programy.triggers.local.LocalTriggerManager", triggers_config.manager)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEqual("programy.triggers.local.LocalTriggerManager", triggers_config.manager)

    def test_with_additional_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            triggers:
                manager: programy.triggers.rest.RestTriggerManager
                url: http://localhost:8989/api/v1.0/trigger
                method: POST
                token: 123BC4F3D
        """, ConsoleConfiguration(), ".")

        console_config = yaml.get_section("console")

        triggers_config = TriggerConfiguration()
        triggers_config.load_config_section(yaml, console_config, ".")

        self.assertEqual("programy.triggers.rest.RestTriggerManager", triggers_config.manager)
        self.assertEqual(triggers_config.value("url"), "http://localhost:8989/api/v1.0/trigger")
        self.assertEqual(triggers_config.value("method"), "POST")
        self.assertEqual(triggers_config.value("token"), "123BC4F3D")

    def test_to_yaml_no_defaults(self):
        triggers_config = TriggerConfiguration()
        triggers_config._manager = "programy.triggers.local.LocalTriggerManager2"

        data = {}
        triggers_config.to_yaml(data, defaults=False)
        self.assertEquals({'manager': 'programy.triggers.local.LocalTriggerManager2'}, data)

    def test_to_yaml_with_defaults(self):
        triggers_config = TriggerConfiguration()
        triggers_config._manager = TriggerConfiguration.LOCAL_MANAGER

        data = {}
        triggers_config.to_yaml(data, defaults=True)
        self.assertEquals({'manager': 'programy.triggers.local.LocalTriggerManager'}, data)

    def test_defaults(self):
        triggers_config = TriggerConfiguration()
        data = {}
        triggers_config.to_yaml(data, True)

        TriggersConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['manager'], TriggerConfiguration.LOCAL_MANAGER)
