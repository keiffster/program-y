import unittest.mock

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLStorageConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):
        config = SQLStorageConfiguration()
        self.assertEqual(config.url, 'sqlite:///:memory:')
        self.assertEqual(config.echo, False)
        self.assertEqual(config.encoding, 'utf-8')
        self.assertEqual(config.create_db, True)
        self.assertEqual(config.drop_all_first, True)

    def test_change_values(self):
        config = SQLStorageConfiguration()
        config.url = "mysql://test"
        config.create_db = False
        config.drop_all_first = False

        self.assertEqual(config.url, "mysql://test")
        self.assertEqual(config.create_db, False)
        self.assertEqual(config.drop_all_first, False)

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

    def test_initialise_with_config_no_data(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                sql:
                    type:   sql
                    config:
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("sql")

        config = SQLStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual(config.url, 'sqlite:///:memory:')
        self.assertEqual(config.echo, False)
        self.assertEqual(config.encoding, 'utf-8')
        self.assertEqual(config.create_db, True)
        self.assertEqual(config.drop_all_first, True)

    def test_initialise_no_config_no_data(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                sql:
                    type:   sql
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("sql")

        config = SQLStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual(config.url, 'sqlite:///:memory:')
        self.assertEqual(config.echo, False)
        self.assertEqual(config.encoding, 'utf-8')
        self.assertEqual(config.create_db, True)
        self.assertEqual(config.drop_all_first, True)

    def test_create_sqlstorage_config(self):

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

        self.assertEqual({'create_db': True, 'drop_all_first': True, 'echo': False, 'encoding': 'utf-8', 'url': 'sqlite:///:memory:'}, config.create_sqlstorage_config())

    def test_create_sqlstorage_config_not_memory(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                sql:
                    type:   sql
                    config:
                        url: sql:///:other
                        echo: false
                        encoding: utf-8
                        create_db: true
                        drop_all_first: True
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("sql")

        config = SQLStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual({'create_db': True, 'drop_all_first': True, 'echo': False, 'encoding': 'utf-8', 'url': 'sql:///:other'}, config.create_sqlstorage_config())

    def test_to_yaml_with_defaults(self):
        config = SQLStorageConfiguration()

        data = {}
        config.to_yaml(data, defaults=True)
        self.assertEqual({'create_db': True, 'drop_all_first': True, 'echo': False, 'encoding': 'utf-8', 'url': 'sqlite:///:memory:'}, data)

    def test_to_yaml_no_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                sql:
                    type:   sql
                    config:
                        url: sqlite:///:memory
                        echo: True
                        encoding: ascii-8
                        create_db: false
                        drop_all_first: false
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("sql")

        config = SQLStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        data = {}
        config.to_yaml(data, defaults=False)
        self.assertEqual({'create_db': False, 'drop_all_first': False, 'echo': True, 'encoding': 'ascii-8', 'url': 'sqlite:///:memory:'}, data)
