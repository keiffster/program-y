import unittest

from programy.storage.factory import StorageFactory

from programy.config.file.yaml_file import YamlConfigurationFile

from programy.storage.config import StorageConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.logger.engine import LoggerStorageEngine
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine


class StorageFactoryTests(unittest.TestCase):

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            storage:
                entities:
                    users: sql
                    linked_accounts: sql
                    links: sql
                    properties: redis
                    conversations:   mongo
                    categories: sql

                stores:
                    sql:
                        type:   sql
                        config:
                            url: sqlite:///:memory
                            echo: false
                            encoding: utf-8
                            create_db: true
                            drop_all_first: true

                    mongo:
                        type:   mongo
                        config:
                            url: mongodb://localhost:27017/
                            database: programy
                            drop_all_first: true

                    redis:
                        type:   redis
                        config:
                            host: localhost
                            port: 6379
                            password: null
                            db: 0
                            prefix: programy
                            drop_all_first: True            

                    file:
                        type:   file
                        config:
                            storage_dir: ./storage
                            properties_storage: ./storage/properties
                            conversation_storage: ./storage/conversations

                    logger:
                        type:   logger
                        config:
                            conversation_logger: conversation

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        storage_config = StorageConfiguration()
        storage_config.load_config_section(yaml, bot_config, ".")

        factory = StorageFactory()
        factory.load_engines_from_config(storage_config)

        self.assertTrue(factory.storage_engine_available("sql"))
        self.assertIsInstance(factory.storage_engine("sql"), SQLStorageEngine)
        self.assertTrue(factory.storage_engine_available("mongo"))
        self.assertIsInstance(factory.storage_engine("mongo"), MongoStorageEngine)
        self.assertTrue(factory.storage_engine_available("redis"))
        self.assertIsInstance(factory.storage_engine("redis"), RedisStorageEngine)
        self.assertTrue(factory.storage_engine_available("file"))
        self.assertIsInstance(factory.storage_engine("file"), FileStorageEngine)
        self.assertTrue(factory.storage_engine_available("logger"))
        self.assertIsInstance(factory.storage_engine("logger"), LoggerStorageEngine)
        self.assertFalse(factory.storage_engine_available("other"))
        self.assertIsNone(factory.storage_engine("other"))

        self.assertTrue(factory.entity_storage_engine_available("users"))
        self.assertIsInstance(factory.entity_storage_engine("users"), SQLStorageEngine)
        self.assertTrue(factory.entity_storage_engine_available("linked_accounts"))
        self.assertIsInstance(factory.entity_storage_engine("linked_accounts"), SQLStorageEngine)
        self.assertTrue(factory.entity_storage_engine_available("links"))
        self.assertIsInstance(factory.entity_storage_engine("links"), SQLStorageEngine)
        self.assertTrue(factory.entity_storage_engine_available("properties"))
        self.assertIsInstance(factory.entity_storage_engine("properties"), RedisStorageEngine)
        self.assertTrue(factory.entity_storage_engine_available("conversations"))
        self.assertIsInstance(factory.entity_storage_engine("conversations"), MongoStorageEngine)
        self.assertTrue(factory.entity_storage_engine_available("categories"))
        self.assertIsInstance(factory.entity_storage_engine("categories"), SQLStorageEngine)
        self.assertFalse(factory.entity_storage_engine_available("other"))
        self.assertIsNone(factory.entity_storage_engine("other"))

