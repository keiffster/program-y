import unittest

from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration

class MongoStorgeConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):
        config = MongoStorageConfiguration()
        self.assertIsNotNone(config)
        self.assertTrue(config.url.startswith('mongodb://localhost:'))
        self.assertEqual(config.database, "programy")
        self.assertEqual(config.drop_all_first, True)

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
