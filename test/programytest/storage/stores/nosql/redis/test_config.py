import unittest

from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration

class RedisStorageConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):
        config = RedisStorageConfiguration()
        self.assertIsNotNone(config)
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 6379)
        self.assertEqual(config.password, None)
        self.assertEqual(config.db, 0)
        self.assertEqual(config.prefix, "programy")
        self.assertEqual(config.drop_all_first, True)

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            redis:
                type:   redis
                config:
                    host: localhost
                    port: 6379
                    password: passwordX
                    db: 0
                    prefix: programy
                    drop_all_first: True            
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("redis")

        config = RedisStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 6379)
        self.assertEqual(config.password, "passwordX")
        self.assertEqual(config.db, 0)
        self.assertEqual(config.prefix, "programy")
        self.assertEqual(config.drop_all_first, True)
