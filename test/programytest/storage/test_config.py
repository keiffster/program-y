import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.config import StorageConfiguration
from programy.storage.factory import StorageFactory


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

    def test_create_storage_config_all(self):
        storage_config = StorageConfiguration()

        config = storage_config.create_storage_config(file=True, sqlite=True, mongo=True, redis=True, logger=True)
        self.assertIsNotNone(config)

        self.assertTrue('file' in config['stores'])
        self.assertTrue('sqlite' in config['stores'])
        self.assertTrue('mongo' in config['stores'])
        self.assertTrue('redis' in config['stores'])
        self.assertTrue('logger' in config['stores'])

    def test_to_yaml_defaults(self):
        storage_config = StorageConfiguration()

        data = {}
        storage_config.to_yaml(data, defaults=True)

        self.assertEquals({'entities': {'categories': 'file', 'errors': 'file', 'duplicates': 'file', 'learnf': 'file',
                                        'conversations': 'file', 'maps': 'file', 'sets': 'file', 'rdf': 'file',
                                        'denormal': 'file', 'normal': 'file', 'gender': 'file', 'person': 'file',
                                        'person2': 'file', 'regex_templates': 'file', 'properties': 'file',
                                        'defaults': 'file', 'variables': 'file', 'twitter': 'file',
                                        'spelling_corpus': 'file', 'license_keys': 'file', 'pattern_nodes': 'file',
                                        'template_nodes': 'file', 'binaries': 'file', 'braintree': 'file',
                                        'preprocessors': 'file', 'postprocessors': 'file',
                                        'postquestionprocessors': 'file', 'usergroups': 'file', 'triggers': 'file'},
                           'stores': {'file': {
                               'categories_storage': {'dirs': ['/tmp/categories'], 'extension': 'aiml', 'subdirs': True,
                                                      'file': None, 'format': 'xml', 'encoding': 'utf-8',
                                                      'delete_on_start': False},
                               'errors_storage': {'dirs': ['/tmp/debug/errors.txt'], 'extension': None,
                                                  'subdirs': False, 'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                  'delete_on_start': False},
                               'duplicates_storage': {'dirs': ['/tmp/debug/duplicates.txt'], 'extension': None,
                                                      'subdirs': False, 'file': None, 'format': 'text',
                                                      'encoding': 'utf-8', 'delete_on_start': False},
                               'learnf_storage': {'dirs': ['/tmp/categories/learnf'], 'extension': 'aiml',
                                                  'subdirs': False, 'file': None, 'format': 'xml', 'encoding': 'utf-8',
                                                  'delete_on_start': False},
                               'conversation_storage': {'dirs': ['/tmp/conversations'], 'extension': 'txt',
                                                        'subdirs': False, 'file': None, 'format': 'text',
                                                        'encoding': 'utf-8', 'delete_on_start': False},
                               'sets_storage': {'dirs': ['/tmp/sets'], 'extension': 'txt', 'subdirs': False,
                                                'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                'delete_on_start': False},
                               'maps_storage': {'dirs': ['/tmp/maps'], 'extension': 'txt', 'subdirs': False,
                                                'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                'delete_on_start': False},
                               'rdf_storage': {'dirs': ['/tmp/rdfs'], 'extension': 'txt', 'subdirs': True, 'file': None,
                                               'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                               'denormal_storage': {'dirs': ['/tmp/lookups/denormal.txt'], 'extension': None,
                                                    'subdirs': False, 'file': None, 'format': 'text',
                                                    'encoding': 'utf-8', 'delete_on_start': False},
                               'normal_storage': {'dirs': ['/tmp/lookups/normal.txt'], 'extension': None,
                                                  'subdirs': False, 'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                  'delete_on_start': False},
                               'gender_storage': {'dirs': ['/tmp/lookups/gender.txt'], 'extension': None,
                                                  'subdirs': False, 'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                  'delete_on_start': False},
                               'person_storage': {'dirs': ['/tmp/lookups/person.txt'], 'extension': None,
                                                  'subdirs': False, 'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                  'delete_on_start': False},
                               'person2_storage': {'dirs': ['/tmp/lookups/person2.txt'], 'extension': None,
                                                   'subdirs': False, 'file': None, 'format': 'text',
                                                   'encoding': 'utf-8', 'delete_on_start': False},
                               'regex_storage': {'dirs': ['/tmp/lookups/regex.txt'], 'extension': None,
                                                 'subdirs': False, 'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                 'delete_on_start': False},
                               'properties_storage': {'dirs': ['/tmp/properties.txt'], 'extension': None,
                                                      'subdirs': False, 'file': None, 'format': 'text',
                                                      'encoding': 'utf-8', 'delete_on_start': False},
                               'defaults_storage': {'dirs': ['/tmp/defaults.txt'], 'extension': None, 'subdirs': False,
                                                    'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                    'delete_on_start': False},
                               'twitter_storage': {'dirs': ['/tmp/twitter'], 'extension': 'txt', 'subdirs': False,
                                                   'file': None, 'format': 'text', 'encoding': 'utf-8',
                                                   'delete_on_start': False},
                               'spelling_storage': {'dirs': ['/tmp/spelling/corpus.txt'], 'extension': None,
                                                    'subdirs': False, 'file': None, 'format': 'text',
                                                    'encoding': 'utf-8', 'delete_on_start': False},
                               'license_storage': {'dirs': ['/tmp/licenses/license.keys'], 'extension': None,
                                                   'subdirs': False, 'file': None, 'format': 'text',
                                                   'encoding': 'utf-8', 'delete_on_start': False},
                               'pattern_nodes_storage': {'dirs': ['/tmp/nodes/pattern_nodes.txt'], 'extension': None,
                                                         'subdirs': False, 'file': None, 'format': 'text',
                                                         'encoding': 'utf-8', 'delete_on_start': False},
                               'template_nodes_storage': {'dirs': ['/tmp/nodes/template_nodes.txt'], 'extension': None,
                                                          'subdirs': False, 'file': None, 'format': 'text',
                                                          'encoding': 'utf-8', 'delete_on_start': False},
                               'binaries_storage': {'dirs': ['/tmp/braintree/braintree.bin'], 'extension': None,
                                                    'subdirs': False, 'file': None, 'format': 'binary',
                                                    'encoding': 'utf-8', 'delete_on_start': False},
                               'braintree_storage': {'dirs': ['/tmp/braintree/braintree.xml'], 'extension': None,
                                                     'subdirs': False, 'file': None, 'format': 'xml',
                                                     'encoding': 'utf-8', 'delete_on_start': False},
                               'preprocessors_storage': {'dirs': ['/tmp/processing/preprocessors.conf'],
                                                         'extension': None, 'subdirs': False, 'file': None,
                                                         'format': 'text', 'encoding': 'utf-8',
                                                         'delete_on_start': False},
                               'postprocessors_storage': {'dirs': ['/tmp/processing/postprocessors.conf'],
                                                          'extension': None, 'subdirs': False, 'file': None,
                                                          'format': 'text', 'encoding': 'utf-8',
                                                          'delete_on_start': False}, 'postquestionprocessors_storage': {
                                   'dirs': ['/tmp/processing/postquestionprocessors.conf'], 'extension': None,
                                   'subdirs': False, 'file': None, 'format': 'text', 'encoding': 'utf-8',
                                   'delete_on_start': False},
                               'usergroups_storage': {'dirs': ['/tmp/security/usergroups.txt'], 'extension': None,
                                                      'subdirs': False, 'file': None, 'format': 'text',
                                                      'encoding': 'utf-8', 'delete_on_start': False},
                               'triggers_storage': {'dirs': ['/tmp/triggers/triggers.txt'], 'extension': None,
                                                    'subdirs': False, 'file': None, 'format': 'text',
                                                    'encoding': 'utf-8', 'delete_on_start': False}}}}
                          , data)
