"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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

    def check_for_license_keys(self, license_keys):
        BaseConfigurationData.check_for_license_keys(self, license_keys)

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
                    YLogger.error(None, "'type' section missing from client config stores element [%s], ignoring config", store)
                    continue

                if 'config' not in keys:
                    YLogger.error(None, "'config' section missing from client config stores element [%s], ignoring config", store)
                    continue

                type = configuration_file.get_option(store_config, 'type', subs=subs)

                if type == 'sql':
                    config = SQLStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)

                elif type == 'mongo':
                    config = MongoStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)

                elif type == 'redis':
                    config = RedisStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)

                elif type == 'file':
                    config = FileStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)

                elif type == 'logger':
                    config = LoggerStorageConfiguration()
                    config.load_config_section(configuration_file, store_config, bot_root, subs=subs)

                self._store_configs[store] = config

        else:
            YLogger.warning(self, "'storage' section missing from client config, using to defaults")

            self._entity_store = {}
            self.add_default_entities(self._entity_store)

            self._store_configs = {}
            self.add_default_stores(self._store_configs)

    def create_storage_config(self):
        config = {}
        config['entities'] = {}
        self.add_default_entities(config['entities'])

        config['stores'] = {}
        self.add_default_stores(config['stores'])

    def to_yaml(self, data, defaults=True):

        data['entities'] = {}
        data['stores'] = {}

        if defaults is True:
            self.add_default_entities(data['entities'])
            self.add_default_stores(data['stores'])
        else:
            data['entities'] = {}
            for key, value in self._entity_store.items():
                data['entities'][key] = value

            for name, value in self._store_configs.items():
                data['stores'][name] = {}
                value.to_yaml(data['stores'][name], defaults)

    @staticmethod
    def add_default_stores(amap):
        
        sql = SQLStorageConfiguration()
        amap['sqlite'] = {'type': 'sql',
                        'config': sql.create_sqlstorage_config()}

        mongo = MongoStorageConfiguration()
        amap['mongo'] = {'type': 'mongo',
                         'config': mongo.create_mongostorage_config()}

        redis = RedisStorageConfiguration()
        amap['redis'] = {'type': 'redis',
                         'config': redis.create_redisstorage_config()}

        file = FileStorageConfiguration()
        amap['file'] = {'type': 'file',
                        'config': file.create_filestorage_config()}

        logger = LoggerStorageConfiguration()
        amap['logger'] = {'type': 'logger',
                          'config': logger.create_loggerstorage_config()}

    @staticmethod
    def add_default_entities(amap):

        amap[StorageFactory.USERS] = 'sqlite'
        amap[StorageFactory.LINKED_ACCOUNTS] = 'sqlite'
        amap[StorageFactory.LINKS] = 'sqlite'

        amap[StorageFactory.CATEGORIES] = 'file'
        amap[StorageFactory.ERRORS] = 'file'
        amap[StorageFactory.DUPLICATES] = 'file'
        amap[StorageFactory.LEARNF] = 'file'

        amap[StorageFactory.CONVERSATIONS] = 'file'

        amap[StorageFactory.MAPS] = 'file'
        amap[StorageFactory.SETS] = 'file'
        amap[StorageFactory.RDF] = 'file'

        amap[StorageFactory.DENORMAL] = 'file'
        amap[StorageFactory.NORMAL] = 'file'
        amap[StorageFactory.GENDER] = 'file'
        amap[StorageFactory.PERSON] = 'file'
        amap[StorageFactory.PERSON2] = 'file'
        amap[StorageFactory.REGEX_TEMPLATES] = 'file'

        amap[StorageFactory.PROPERTIES] = 'file'
        amap[StorageFactory.DEFAULTS] = 'file'
        amap[StorageFactory.VARIABLES] = 'file'

        amap[StorageFactory.TWITTER] = 'file'

        amap[StorageFactory.SPELLING_CORPUS] = 'file'

        amap[StorageFactory.LICENSE_KEYS] = 'file'

        amap[StorageFactory.PATTERN_NODES] = 'file'
        amap[StorageFactory.TEMPLATE_NODES] = 'file'

        amap[StorageFactory.BINARIES] = 'file'
        amap[StorageFactory.BRAINTREE] = 'file'

        amap[StorageFactory.PREPROCESSORS] = 'file'
        amap[StorageFactory.POSTPROCESSORS] = 'file'

        amap[StorageFactory.USERGROUPS] = 'file'

        amap[StorageFactory.TRIGGERS] = 'file'
