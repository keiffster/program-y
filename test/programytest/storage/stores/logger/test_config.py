import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.stores.logger.config import LoggerStorageConfiguration


class LoggerStorageConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):

        config = LoggerStorageConfiguration()
        self.assertIsNotNone(config)

        self.assertEqual("conversation", config.conversation_logger)

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                logger:
                    type:   logger
                    config:
                        conversation_logger: conversations
                """, ConsoleConfiguration(), ".")

        logger_config = yaml.get_section("logger")

        config = LoggerStorageConfiguration()
        config.load_config_section(yaml, logger_config, ".")

        self.assertEqual("conversations", config.conversation_logger)

    def test_initialise_with_config_no_data(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                logger:
                """, ConsoleConfiguration(), ".")

        logger_config = yaml.get_section("logger")

        config = LoggerStorageConfiguration()
        config.load_config_section(yaml, logger_config, ".")

        self.assertEqual("conversation", config.conversation_logger)

    def test_initialise_with_no_config_no_data(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                other:
                """, ConsoleConfiguration(), ".")

        logger_config = yaml.get_section("logger")

        config = LoggerStorageConfiguration()
        config.load_config_section(yaml, logger_config, ".")

        self.assertEqual("conversation", config.conversation_logger)

    def test_create_loggerstorage_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                logger:
                    type:   logger
                    config:
                        conversation_logger: conversations
                """, ConsoleConfiguration(), ".")

        logger_config = yaml.get_section("logger")

        config = LoggerStorageConfiguration()
        config.load_config_section(yaml, logger_config, ".")

        self.assertEquals({'conversation_logger': 'conversations'}, config.create_loggerstorage_config())

    def test_to_yaml_defaults(self):
        config = LoggerStorageConfiguration()
        data = {}
        config.to_yaml(data, True)
        self.assertEquals({'conversation_logger': 'conversation'}, data)

    def test_to_yaml_no_defaults(self):
        config = LoggerStorageConfiguration()
        config._conversation_logger = "convologger"
        data = {}
        config.to_yaml(data, False)
        self.assertEquals({'conversation_logger': 'convologger'}, data)
