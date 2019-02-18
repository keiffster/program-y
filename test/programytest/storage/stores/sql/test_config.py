import unittest
import unittest.mock

from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration

class SQLStorageConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):
        config = SQLStorageConfiguration()
        self.assertEqual(config.url, 'sqlite:///:memory:')
        self.assertEqual(config.echo, False)
        self.assertEqual(config.encoding, 'utf-8')
        self.assertEqual(config.create_db, True)
        self.assertEqual(config.drop_all_first, True)

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                sql:
                    type:   sql
                    config:
                        url: sqlite:///:memory
                        echo: false
                        encoding: utf-8
                        create_db: true
                        drop_all_first: True
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("sql")

        config = SQLStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual(config.url, 'sqlite:///:memory:')
        self.assertEqual(config.echo, False)
        self.assertEqual(config.encoding, 'utf-8')
        self.assertEqual(config.create_db, True)
        self.assertEqual(config.drop_all_first, True)
