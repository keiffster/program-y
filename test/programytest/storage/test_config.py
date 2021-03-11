import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.config import StorageConfiguration
from programy.storage.factory import StorageFactory
from programytest.storage.stores.file.test_config import FileStorageConfigurationTests


class StorageConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            storage:
                entities:
                    users: sqlite
                    linked_accounts: sqlite
                    links: sqlite
                    
                    categories: file
                    errors: file
                    duplicates: file
                    learnf: file

                    conversations: file

                    maps: file
                    sets: file
                    rdf: file
                    
                    denormal: file
                    normal: file
                    gender: file
                    person: file
                    person2: file
                    regex_templates: file

                    properties: file
                    variables: file
                    defaults: file

                    twitter: file

                    spelling_corpus: file

                    license_keys: file
                    
                    template_nodes: file
                    pattern_nodes: file
                    
                    binaries: file
                    braintree: file
                    
                    preprocessors: file
                    postprocessors: file
                    
                    usergroups: file
                
                    triggers: file
                    
                    oobs: file
                    
                    services: file
                    
                stores:
                    sqlite:
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
                            password: None
                            db: 0
                            prefix: programy
                            drop_all_first: True            
                
                    file:
                        type:   file
                        config:
                            properties_storage: 
                                file: ./storage/properties
                            conversation_storage: 
                                dir: ./storage/conversations
            
                    logger:
                        type:   logger
                        config:
                            conversation_logger: conversation
                            
                    other:
                        other:  For test only

                    other2:
                        type:   other

                    other3:
                        type:   other3
                        config:
                            something: other

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        storage_config = StorageConfiguration()
        storage_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNotNone(storage_config.entity_store)
        self.assert_entity_store(storage_config)

        self.assertIsNotNone(storage_config.storage_configurations)
        self.assert_storage_configurations(storage_config)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            storage:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        storage_config = StorageConfiguration()
        storage_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNotNone(storage_config.entity_store)
        self.assert_entity_store(storage_config)

        self.assertIsNotNone(storage_config.storage_configurations)
        self.assert_storage_configurations(storage_config)

    def test_with_no_data_no_config(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        storage_config = StorageConfiguration()
        storage_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNotNone(storage_config.entity_store)
        self.assert_entity_store(storage_config)

        self.assertIsNotNone(storage_config.storage_configurations)
        self.assert_storage_configurations(storage_config)

    def assert_entity_store(self, storage_config, file=True, sqllite=False):

        if sqllite is True:
            self.assertEqual(storage_config.entity_store[StorageFactory.USERS], 'sqlite')
            self.assertEqual(storage_config.entity_store[StorageFactory.LINKED_ACCOUNTS], 'sqlite')
            self.assertEqual(storage_config.entity_store[StorageFactory.LINKS], 'sqlite')

        if file is True:
            self.assertEqual(storage_config.entity_store[StorageFactory.CATEGORIES], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.ERRORS], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.DUPLICATES], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.LEARNF], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.CONVERSATIONS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.MAPS], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.SETS], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.RDF], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.DENORMAL], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.NORMAL], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.GENDER], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.PERSON], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.PERSON2], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.REGEX_TEMPLATES], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.PROPERTIES], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.DEFAULTS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.TWITTER], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.SPELLING_CORPUS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.LICENSE_KEYS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.TEMPLATE_NODES], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.PATTERN_NODES], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.BINARIES], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.BRAINTREE], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.PREPROCESSORS], 'file')
            self.assertEqual(storage_config.entity_store[StorageFactory.POSTPROCESSORS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.USERGROUPS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.TRIGGERS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.OOBS], 'file')

            self.assertEqual(storage_config.entity_store[StorageFactory.SERVICES], 'file')

    def assert_storage_configurations(self, storage_config, file=True, sqlite=False, mongo=False, redis=False, logger=False):

        if sqlite is True:
            self.assertTrue('sqlite' in storage_config.storage_configurations)
        if mongo is True:
            self.assertTrue('mongo' in storage_config.storage_configurations)
        if redis is True:
            self.assertTrue('redis' in storage_config.storage_configurations)
        if file is True:
            self.assertTrue('file' in storage_config.storage_configurations)
        if logger is True:
            self.assertTrue('logger' in storage_config.storage_configurations)

    def test_create_storage_config_file_only(self):
        storage_config = StorageConfiguration()

        config = storage_config.create_storage_config()
        self.assertIsNotNone(config)

        self.assertTrue('file' in config['stores'])
        self.assertFalse('sqlite' in config['stores'])
        self.assertFalse('mongo' in config['stores'])
        self.assertFalse('redis' in config['stores'])
        self.assertFalse('logger' in config['stores'])

    def test_create_storage_config_nothing(self):
        storage_config = StorageConfiguration()

        config = storage_config.create_storage_config(file=False, sqlite=False, mongo=False, redis=False, logger=False)
        self.assertIsNotNone(config)

        self.assertFalse('file' in config['stores'])
        self.assertFalse('sqlite' in config['stores'])
        self.assertFalse('mongo' in config['stores'])
        self.assertFalse('redis' in config['stores'])
        self.assertFalse('logger' in config['stores'])

    def test_create_storage_config_all(self):
        storage_config = StorageConfiguration()

        config = storage_config.create_storage_config(file=True, sqlite=True, mongo=True, redis=True, logger=True)
        self.assertIsNotNone(config)

        self.assertTrue('file' in config['stores'])
        self.assertTrue('sqlite' in config['stores'])
        self.assertTrue('mongo' in config['stores'])
        self.assertTrue('redis' in config['stores'])
        self.assertTrue('logger' in config['stores'])

    def test_to_yaml_no_defaults_not_empty(self):
        storage_config = StorageConfiguration()

        StorageConfiguration.add_default_entities(storage_config._entity_store)
        StorageConfiguration.add_default_stores_as_yaml(storage_config._store_configs)

        data = {}
        storage_config.to_yaml(data, defaults=False)

        self.assertDefaultEntities(data['entities'])
        self.assertDefaultFileStoreConfig(data['stores'])

    def test_to_yaml_no_defaults_empty(self):
        storage_config = StorageConfiguration()

        data = {}
        storage_config.to_yaml(data, defaults=False)

        self.assertEquals({'entities': {}, 'stores': {}}, data)

    def test_to_yaml_defaults(self):
        storage_config = StorageConfiguration()

        data = {}
        storage_config.to_yaml(data, defaults=True)

        self.assertDefaultEntities(data['entities'])
        self.assertDefaultFileStoreConfig(data['stores'])

    def test_add_default_stores_all_off(self):
        store_configs = {}
        StorageConfiguration.add_default_stores_as_yaml(store_configs, file=False, sqlite=False, mongo=False, redis=False, logger=False)
        self.assertEquals({}, store_configs)

    def test_add_default_stores_all_on(self):
        store_configs = {}
        StorageConfiguration.add_default_stores_as_yaml(store_configs, file=True, sqlite=True, mongo=True, redis=True, logger=True)

        self.assertDefaultStoreConfigs(store_configs)

    def assertDefaultEntities(self, entities):
        self.assertEqual("file", entities['categories'])
        self.assertEqual("file", entities['errors'])
        self.assertEqual("file", entities['duplicates'])
        self.assertEqual("file", entities['learnf'])
        self.assertEqual("file", entities['conversations'])
        self.assertEqual("file", entities['maps'])
        self.assertEqual("file", entities['sets'])
        self.assertEqual("file", entities['rdf'])
        self.assertEqual("file", entities['denormal'])
        self.assertEqual("file", entities['normal'])
        self.assertEqual("file", entities['gender'])
        self.assertEqual("file", entities['person'])
        self.assertEqual("file", entities['person2'])
        self.assertEqual("file", entities['regex_templates'])
        self.assertEqual("file", entities['properties'])
        self.assertEqual("file", entities['defaults'])
        self.assertEqual("file", entities['variables'])
        self.assertEqual("file", entities['twitter'])
        self.assertEqual("file", entities['spelling_corpus'])
        self.assertEqual("file", entities['license_keys'])
        self.assertEqual("file", entities['pattern_nodes'])
        self.assertEqual("file", entities['template_nodes'])
        self.assertEqual("file", entities['binaries'])
        self.assertEqual("file", entities['braintree'])
        self.assertEqual("file", entities['preprocessors'])
        self.assertEqual("file", entities['postprocessors'])
        self.assertEqual("file", entities['postquestionprocessors'])
        self.assertEqual("file", entities['usergroups'])
        self.assertEqual("file", entities['triggers'])
        self.assertEqual("file", entities['oobs'])
        self.assertEqual("file", entities['services'])

    def assertDefaultStoreConfigs(self, store_configs):
        self.assertDefaultFileStoreConfig(store_configs)
        self.assertDefaultSQLStoreConfig(store_configs)
        self.assertDefaultMongoStoreConfig(store_configs)
        self.assertDefaultRedisStoreConfig(store_configs)
        self.assertDefaultLoggerStoreConfig(store_configs)

    def assertDefaultFileStoreConfig(self, store_configs):
        self.assertTrue('file' in store_configs)
        self.assertTrue('type' in store_configs['file'])
        self.assertEquals('file', store_configs['file']['type'])
        self.assertTrue('config' in store_configs['file'])
        config = store_configs['file']['config']

        self.assertIsNotNone(config)
        self.assertTrue('categories_storage'in config)
        self.assertTrue('errors_storage'in config)
        self.assertTrue('duplicates_storage'in config)
        self.assertTrue('learnf_storage'in config)
        self.assertTrue('conversation_storage'in config)
        self.assertTrue('sets_storage'in config)
        self.assertTrue('maps_storage'in config)
        self.assertTrue('rdf_storage'in config)
        self.assertTrue('denormal_storage'in config)
        self.assertTrue('normal_storage'in config)
        self.assertTrue('gender_storage'in config)
        self.assertTrue('person_storage'in config)
        self.assertTrue('person2_storage'in config)
        self.assertTrue('regex_storage'in config)
        self.assertTrue('properties_storage'in config)
        self.assertTrue('defaults_storage'in config)
        self.assertTrue('twitter_storage'in config)
        self.assertTrue('spelling_storage'in config)
        self.assertTrue('license_storage'in config)
        self.assertTrue('pattern_nodes_storage'in config)
        self.assertTrue('template_nodes_storage'in config)
        self.assertTrue('binaries_storage'in config)
        self.assertTrue('braintree_storage'in config)
        self.assertTrue('preprocessors_storage'in config)
        self.assertTrue('postprocessors_storage'in config)
        self.assertTrue('postquestionprocessors_storage'in config)
        self.assertTrue('usergroups_storage'in config)
        self.assertTrue('triggers_storage'in config)
        self.assertTrue('oobs_storage'in config)
        self.assertTrue('services_storage'in config)

        self.assertEquals(config['categories_storage'],
                          {'dirs': ['/tmp/categories'], 'extension': 'aiml', 'subdirs': True, 'format': 'xml',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['errors_storage'],
                          {'file': '/tmp/debug/errors.txt', 'extension': None, 'subdirs': False, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['duplicates_storage'],
                          {'file': '/tmp/debug/duplicates.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['learnf_storage'],
                          {'dirs': ['/tmp/categories/learnf'], 'extension': 'aiml', 'subdirs': False,
                           'format': 'xml', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['conversation_storage'],
                          {'dirs': ['/tmp/conversations'], 'extension': 'txt', 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['sets_storage'],
                          {'dirs': ['/tmp/sets'], 'extension': 'txt', 'subdirs': False, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['maps_storage'],
                          {'dirs': ['/tmp/maps'], 'extension': 'txt', 'subdirs': False, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['rdf_storage'],
                          {'dirs': ['/tmp/rdfs'], 'extension': 'txt', 'subdirs': True, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['denormal_storage'],
                          {'file': '/tmp/lookups/denormal.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['normal_storage'],
                          {'file': '/tmp/lookups/normal.txt', 'extension': None, 'subdirs': False, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['gender_storage'],
                          {'file': '/tmp/lookups/gender.txt', 'extension': None, 'subdirs': False, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['person_storage'],
                          {'file': '/tmp/lookups/person.txt', 'extension': None, 'subdirs': False, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['person2_storage'],
                          {'file': '/tmp/lookups/person2.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['regex_storage'],
                          {'file': '/tmp/regex/regex-templates.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['properties_storage'],
                          {'file': '/tmp/properties/properties.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['defaults_storage'],
                          {'file': '/tmp/properties/defaults.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['twitter_storage'],
                          {'dirs': ['/tmp/twitter'], 'extension': 'txt', 'subdirs': False, 'format': 'text',
                           'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['spelling_storage'],
                          {'file': '/tmp/spelling/corpus.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['license_storage'],
                          {'file': '/tmp/licenses/license.keys', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['pattern_nodes_storage'],
                          {'file': '/tmp/nodes/pattern_nodes.conf', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['template_nodes_storage'],
                          {'file': '/tmp/nodes/template_nodes.conf', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['binaries_storage'],
                          {'file': '/tmp/braintree/braintree.bin', 'extension': None, 'subdirs': False,
                           'format': 'binary', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['braintree_storage'],
                          {'file': '/tmp/braintree/braintree.xml', 'extension': None, 'subdirs': False,
                           'format': 'xml', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['preprocessors_storage'],
                          {'file': '/tmp/processing/preprocessors.conf', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['postprocessors_storage'],
                          {'file': '/tmp/processing/postprocessors.conf', 'extension': None,
                           'subdirs': False, 'format': 'text', 'encoding': 'utf-8',
                           'delete_on_start': False})
        self.assertEquals(config['postquestionprocessors_storage'],
                          {'file': '/tmp/processing/postquestionprocessors.conf', 'extension': None,
                           'subdirs': False, 'format': 'text', 'encoding': 'utf-8',
                           'delete_on_start': False})
        self.assertEquals(config['usergroups_storage'],
                          {'file': '/tmp/security/usergroups.yaml', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['triggers_storage'],
                          {'file': '/tmp/triggers/triggers.txt', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['oobs_storage'],
                          {'file': '/tmp/oobs/callmom.conf', 'extension': None, 'subdirs': False,
                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False})
        self.assertEquals(config['services_storage'],
                          {'dirs': ['/tmp/services'], 'extension': 'yaml', 'subdirs': True, 'format': 'yaml',
                           'encoding': 'utf-8', 'delete_on_start': False})

    def assertDefaultSQLStoreConfig(self, store_configs):
        self.assertTrue('sqlite' in store_configs)
        self.assertTrue('type' in store_configs['sqlite'])
        self.assertEquals('sql', store_configs['sqlite']['type'])
        self.assertTrue('config' in store_configs['sqlite'])
        config = store_configs['sqlite']['config']

        self.assertEquals(config, {'url': 'sqlite:///:memory:', 'echo': False, 'encoding': 'utf-8',
                                                    'create_db': True, 'drop_all_first': True})

    def assertDefaultMongoStoreConfig(self, store_configs):
        self.assertTrue('mongo' in store_configs)
        self.assertTrue('type' in store_configs['mongo'])
        self.assertEquals('mongo', store_configs['mongo']['type'])
        self.assertTrue('config' in store_configs['mongo'])
        config = store_configs['mongo']['config']

        self.assertEquals(config, {'url': 'mongodb://localhost:27017/', 'database': 'programy',
                                                   'drop_all_first': True})

    def assertDefaultRedisStoreConfig(self, store_configs):
        self.assertTrue('redis' in store_configs)
        self.assertTrue('type' in store_configs['redis'])
        self.assertEquals('redis', store_configs['redis']['type'])
        self.assertTrue('config' in store_configs['redis'])
        config = store_configs['redis']['config']

        self.assertEquals(config,
                          {'host': 'localhost', 'port': 6379, 'password': None, 'db': 0, 'prefix': 'programy',
                           'drop_all_first': True})

    def assertDefaultLoggerStoreConfig(self, store_configs):
        self.assertTrue('logger' in store_configs)
        self.assertTrue('type' in store_configs['logger'])
        self.assertEquals('logger', store_configs['logger']['type'])
        self.assertTrue('config' in store_configs['logger'])
        config = store_configs['logger']['config']

        self.assertEquals(config, {'conversation_logger': 'conversation'})

    def test_defaults(self):
        storage_config = StorageConfiguration()
        data = {}
        storage_config.to_yaml(data, True)

        StorageConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):

        test.assertTrue('entities' in data)
        test.assertEqual(data['entities'][StorageFactory.CATEGORIES], 'file')
        test.assertEqual(data['entities'][StorageFactory.ERRORS], 'file')
        test.assertEqual(data['entities'][StorageFactory.DUPLICATES], 'file')
        test.assertEqual(data['entities'][StorageFactory.LEARNF], 'file')

        test.assertEqual(data['entities'][StorageFactory.CONVERSATIONS], 'file')

        test.assertEqual(data['entities'][StorageFactory.MAPS], 'file')
        test.assertEqual(data['entities'][StorageFactory.SETS], 'file')
        test.assertEqual(data['entities'][StorageFactory.RDF], 'file')

        test.assertEqual(data['entities'][StorageFactory.DENORMAL], 'file')
        test.assertEqual(data['entities'][StorageFactory.NORMAL], 'file')
        test.assertEqual(data['entities'][StorageFactory.GENDER], 'file')
        test.assertEqual(data['entities'][StorageFactory.PERSON], 'file')
        test.assertEqual(data['entities'][StorageFactory.PERSON2], 'file')
        test.assertEqual(data['entities'][StorageFactory.REGEX_TEMPLATES], 'file')

        test.assertEqual(data['entities'][StorageFactory.PROPERTIES], 'file')
        test.assertEqual(data['entities'][StorageFactory.DEFAULTS], 'file')
        test.assertEqual(data['entities'][StorageFactory.VARIABLES], 'file')

        test.assertEqual(data['entities'][StorageFactory.TWITTER], 'file')

        test.assertEqual(data['entities'][StorageFactory.SPELLING_CORPUS], 'file')

        test.assertEqual(data['entities'][StorageFactory.LICENSE_KEYS], 'file')

        test.assertEqual(data['entities'][StorageFactory.PATTERN_NODES], 'file')
        test.assertEqual(data['entities'][StorageFactory.TEMPLATE_NODES], 'file')

        test.assertEqual(data['entities'][StorageFactory.BINARIES], 'file')
        test.assertEqual(data['entities'][StorageFactory.BRAINTREE], 'file')

        test.assertEqual(data['entities'][StorageFactory.PREPROCESSORS], 'file')
        test.assertEqual(data['entities'][StorageFactory.POSTPROCESSORS], 'file')
        test.assertEqual(data['entities'][StorageFactory.POSTQUESTIONPROCESSORS], 'file')

        test.assertEqual(data['entities'][StorageFactory.USERGROUPS], 'file')

        test.assertEqual(data['entities'][StorageFactory.TRIGGERS], 'file')

        test.assertEqual(data['entities'][StorageFactory.OOBS], 'file')

        test.assertEqual(data['entities'][StorageFactory.SERVICES], 'file')

        test.assertTrue('stores' in data)
        test.assertTrue('file' in data['stores'])
        test.assertTrue('config' in data['stores']['file'])

        FileStorageConfigurationTests.assert_defaults(test, data['stores']['file']['config'])
