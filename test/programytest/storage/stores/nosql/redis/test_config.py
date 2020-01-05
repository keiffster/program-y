import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration


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

    def test_initialise_with_config_no_data(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            redis:
                type:   redis
                config:
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("redis")

        config = RedisStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 6379)
        self.assertEqual(config.password, None)
        self.assertEqual(config.db, 0)
        self.assertEqual(config.prefix, "programy")
        self.assertEqual(config.drop_all_first, True)

    def test_initialise_with_no_config_no_data(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            redis:
                type:   redis
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("redis")

        config = RedisStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 6379)
        self.assertEqual(config.password, None)
        self.assertEqual(config.db, 0)
        self.assertEqual(config.prefix, "programy")
        self.assertEqual(config.drop_all_first, True)

    def test_create_redisstorage_config(self):
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

        self.assertEquals({'db': 0, 'drop_all_first': True, 'host': 'localhost', 'password': 'passwordX', 'port': 6379, 'prefix': 'programy'}, config.create_redisstorage_config())

    def test_to_yaml_no_defaults(self):
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

        data ={}
        config.to_yaml(data, defaults=False)
        self.assertEquals({'db': 0, 'drop_all_first': True, 'host': 'localhost', 'password': None, 'password': 'passwordX', 'port': 6379, 'prefix': 'programy'}, config.create_redisstorage_config())

    def test_to_yaml_with_defaults(self):
        config = RedisStorageConfiguration()

        data ={}
        config.to_yaml(data, defaults=True)
        self.assertEquals({'db': 0, 'drop_all_first': True, 'host': 'localhost', 'password': None, 'port': 6379, 'prefix': 'programy'}, config.create_redisstorage_config())
