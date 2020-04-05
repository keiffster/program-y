import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoStorgeConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):
        config = MongoStorageConfiguration()
        self.assertIsNotNone(config)
        self.assertTrue(config.url.startswith('mongodb://localhost:'))
        self.assertEqual(config.database, "programy")
        self.assertEqual(config.drop_all_first, False)

    def test_getters_setters(self):
        config = MongoStorageConfiguration()

        config.url = 'mongodb://localhost:666/'
        self.assertEquals(config.url, 'mongodb://localhost:666/')

        config.database = "testy"
        self.assertEquals("testy", config.database)

        config.drop_all_first = False
        self.assertFalse(config.drop_all_first)

    def test_create_mongostorage_config_defaults(self):
        config = MongoStorageConfiguration()
        self.assertEquals({'database': 'programy', 'drop_all_first': False, 'url': 'mongodb://localhost:27017/'},
                          config.create_mongostorage_config())

    def test_create_mongostorage_config_no_defaults(self):
        config = MongoStorageConfiguration()
        config.url = 'mongodb://localhost:666/'
        config.database = "testy"
        config.drop_all_first = False

        self.assertEquals({'database': 'testy', 'drop_all_first': False, 'url': 'mongodb://localhost:666/'},
                          config.create_mongostorage_config())

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
               mongo:
                    type:   mongo
                    config:
                        url: mongodb://localhost:27017/
                        database: programy
                        drop_all_first: true
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("mongo")

        config = MongoStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertTrue(config.url.startswith('mongodb://localhost:'))
        self.assertEqual(config.database, "programy")
        self.assertEqual(config.drop_all_first, True)

    def test_initialise_with_config_no_data(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
               mongo:
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("mongo")

        config = MongoStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertTrue(config.url.startswith('mongodb://localhost:'))
        self.assertEqual(config.database, "programy")
        self.assertEqual(config.drop_all_first, False)

    def test_initialise_no_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            other:
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("mongo")

        config = MongoStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertTrue(config.url.startswith('mongodb://localhost:'))
        self.assertEqual(config.database, "programy")
        self.assertEqual(config.drop_all_first, False)

    def test_to_yaml_defaults(self):
        config = MongoStorageConfiguration()

        data = {}
        config.to_yaml(data, defaults=True)

        self.assertEquals({'database': 'programy', 'drop_all_first': True, 'url': 'mongodb://localhost:27017/'}, data)

    def test_to_yaml_no_defaults(self):
        config = MongoStorageConfiguration()

        config.url = 'mongodb://localhost:666/'
        config.database = "testy"
        config.drop_all_first = False

        data = {}
        config.to_yaml(data, defaults=False)

        self.assertEquals({'database': 'testy', 'drop_all_first': False, 'url': 'mongodb://localhost:666/'}, data)