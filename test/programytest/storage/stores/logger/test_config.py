import unittest

from programy.storage.stores.logger.config import LoggerStorageConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration

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
