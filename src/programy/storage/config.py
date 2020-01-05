"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.config.base import BaseConfigurationData
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.logger.config import LoggerStorageConfiguration
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.storage.factory import StorageFactory
from programy.utils.substitutions.substitues import Substitutions


class StorageConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="storage")
        self._entity_store = {}
        self._store_configs = {}

    @property
    def entity_store(self):
        return self._entity_store

    @property
    def storage_configurations(self):
        return self._store_configs

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        storage = configuration_file.get_section(self._section_name, configuration)
        if storage is not None:

            entities = configuration_file.get_section("entities", storage)
            entity_types = configuration_file.get_child_section_keys("entities", storage)
            for entity in entity_types:
                entity_config = configuration_file.get_section(entity, entities)
                self._entity_store[entity] = entity_config

            stores = configuration_file.get_section("stores", storage)
            store_names = configuration_file.get_child_section_keys("stores", storage)
            for store in store_names:
                store_config = configuration_file.get_section(store, stores)
                keys = configuration_file.get_keys(store_config)

                if 'type' not in keys:
                    YLogger.error(None, "'type' section missing from client config stores element [%s], "
                                        "ignoring config", store)
                    continue

                if 'config' not in keys:
                    YLogger.error(None, "'config' section missing from client config stores element [%s], "
                                        "ignoring config", store)
                    continue

                storage_type = configuration_file.get_option(store_config, 'type', subs=subs)

                if storage_type == 'sql':
                    config = SQLStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)
                    self._store_configs[store] = config

                elif storage_type == 'mongo':
                    config = MongoStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)
                    self._store_configs[store] = config

                elif storage_type == 'redis':
                    config = RedisStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)
                    self._store_configs[store] = config

                elif storage_type == 'file':
                    config = FileStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)
                    self._store_configs[store] = config

                elif storage_type == 'logger':
                    config = LoggerStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)
                    self._store_configs[store] = config

                else:
                    YLogger.error(self, "Unknown storage configuration type [%s]", storage_type)

        else:
            YLogger.warning(self, "'storage' section missing from client config, using to defaults")

            self._entity_store = {}
            StorageConfiguration.add_default_entities(self._entity_store)

            self._store_configs = {}
            StorageConfiguration.add_default_stores(self._store_configs)

    def create_storage_config(self, file=True, sqlite=False, mongo=False, redis=False, logger=False):
        config = {}
        config['entities'] = {}
        StorageConfiguration.add_default_entities(config['entities'], file=file, sqlite=sqlite)

        config['stores'] = {}
        StorageConfiguration.add_default_stores(config['stores'], file=file, sqlite=sqlite, mongo=mongo, redis=redis, logger=logger)

        return config

    @staticmethod
    def add_default_stores(store_configs, file=True, sqlite=False, mongo=False, redis=False, logger=False):
        if sqlite is True:
            store_configs['sqlite'] = SQLStorageConfiguration()
        if mongo is True:
            store_configs['mongo'] = MongoStorageConfiguration()
        if redis is True:
            store_configs['redis'] = RedisStorageConfiguration()
        if file is True:
            store_configs['file'] = FileStorageConfiguration()
        if logger is True:
            store_configs['logger'] = LoggerStorageConfiguration()

    @staticmethod
    def add_default_stores_as_yaml(store_configs, file=True, sqlite=False, mongo=False, redis=False, logger=False):

        if file is True:
            store_configs['file'] = {}
            store_configs['file']['type'] = 'file'
            store_configs['file']['config'] = {}

            store = FileStorageConfiguration()
            store.to_yaml(store_configs['file']['config'], defaults=True)

        if sqlite is True:
            store_configs['sqlite'] = {}
            store = SQLStorageConfiguration()
            store.to_yaml(store_configs['sqlite'], defaults=True)

        if mongo is True:
            store_configs['mongo'] = {}
            store = MongoStorageConfiguration()
            store.to_yaml(store_configs['mongo'], defaults=True)

        if redis is True:
            store_configs['redis'] = {}
            store = RedisStorageConfiguration()
            store.to_yaml(store_configs['redis'], defaults=True)

        if logger is True:
            store_configs['logger'] = {}
            store = LoggerStorageConfiguration()
            store.to_yaml(store_configs['logger'], defaults=True)

    @staticmethod
    def add_default_entities(entity_store, file=True, sqlite=False):

        if sqlite is True:
            entity_store[StorageFactory.USERS] = 'sqlite'
            entity_store[StorageFactory.LINKED_ACCOUNTS] = 'sqlite'
            entity_store[StorageFactory.LINKS] = 'sqlite'

        if file is True:
            entity_store[StorageFactory.CATEGORIES] = 'file'
            entity_store[StorageFactory.ERRORS] = 'file'
            entity_store[StorageFactory.DUPLICATES] = 'file'
            entity_store[StorageFactory.LEARNF] = 'file'

            entity_store[StorageFactory.CONVERSATIONS] = 'file'

            entity_store[StorageFactory.MAPS] = 'file'
            entity_store[StorageFactory.SETS] = 'file'
            entity_store[StorageFactory.RDF] = 'file'

            entity_store[StorageFactory.DENORMAL] = 'file'
            entity_store[StorageFactory.NORMAL] = 'file'
            entity_store[StorageFactory.GENDER] = 'file'
            entity_store[StorageFactory.PERSON] = 'file'
            entity_store[StorageFactory.PERSON2] = 'file'
            entity_store[StorageFactory.REGEX_TEMPLATES] = 'file'

            entity_store[StorageFactory.PROPERTIES] = 'file'
            entity_store[StorageFactory.DEFAULTS] = 'file'
            entity_store[StorageFactory.VARIABLES] = 'file'

            entity_store[StorageFactory.TWITTER] = 'file'

            entity_store[StorageFactory.SPELLING_CORPUS] = 'file'

            entity_store[StorageFactory.LICENSE_KEYS] = 'file'

            entity_store[StorageFactory.PATTERN_NODES] = 'file'
            entity_store[StorageFactory.TEMPLATE_NODES] = 'file'

            entity_store[StorageFactory.BINARIES] = 'file'
            entity_store[StorageFactory.BRAINTREE] = 'file'

            entity_store[StorageFactory.PREPROCESSORS] = 'file'
            entity_store[StorageFactory.POSTPROCESSORS] = 'file'
            entity_store[StorageFactory.POSTQUESTIONPROCESSORS] = 'file'

            entity_store[StorageFactory.USERGROUPS] = 'file'

            entity_store[StorageFactory.TRIGGERS] = 'file'

    def to_yaml(self, data, defaults=True):

        data['entities'] = {}
        data['stores'] = {}

        if defaults is True:
            StorageConfiguration.add_default_entities(data['entities'])
            StorageConfiguration.add_default_stores_as_yaml(data['stores'])

        else:
            data['entities'] = {}
            for key, value in self._entity_store.items():
                data['entities'][key] = value

            for name, value in self._store_configs.items():
                data['stores'][name] = {}
                data['stores'][name] = value

