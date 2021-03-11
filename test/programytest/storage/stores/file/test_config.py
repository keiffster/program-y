import os
import unittest
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.filestore import FileStore
import programytest.storage.engines as Engines


class FileStorageConfigurationTests(unittest.TestCase):

    unittest.skipIf(Engines.file is True, Engines.file_disabled)
    def test_initial_creation_with_defaults(self):

        config = FileStorageConfiguration()
        self.assertIsNotNone(config)

        self.assertIsNotNone(config.categories_storage)
        self.assertIsNotNone(config.learnf_storage)

        self.assertIsNotNone(config.conversation_storage)

        self.assertIsNotNone(config.sets_storage)
        self.assertIsNotNone(config.maps_storage)
        self.assertIsNotNone(config.rdf_storage)

        self.assertIsNotNone(config.denormal_storage)
        self.assertIsNotNone(config.normal_storage)
        self.assertIsNotNone(config.gender_storage)
        self.assertIsNotNone(config.person_storage)
        self.assertIsNotNone(config.person2_storage)
        self.assertIsNotNone(config.regex_storage)

        self.assertIsNotNone(config.properties_storage)
        self.assertIsNotNone(config.defaults_storage)

        self.assertIsNotNone(config.twitter_storage)

        self.assertIsNotNone(config.spelling_storage)
        self.assertIsNotNone(config.license_storage)

        self.assertIsNotNone(config.template_nodes_storage)
        self.assertIsNotNone(config.pattern_nodes_storage)

        self.assertIsNotNone(config.binaries_storage)
        self.assertIsNotNone(config.braintree_storage)

        self.assertIsNotNone(config.preprocessors_storage)
        self.assertIsNotNone(config.postprocessors_storage)
        self.assertIsNotNone(config.postquestionprocessors_storage)

        self.assertIsNotNone(config.usergroups_storage)

        self.assertIsNotNone(config.oobs_storage)

        self.assertIsNotNone(config.triggers_storage)

        self.assertIsNotNone(config.services_storage)

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
              file:
                type:   file
                config:                    
                    categories_storage:
                      dirs: ./storage/categories
                      subdirs: true
                      extension: aiml
                      format: xml
                      encoding: utf-8     
                      delete_on_start: false            
                    learnf_storage:
                      dirs: ./storage/categories/learnf
                      subdirs: false
                      extension: aiml
                      format: xml
                      encoding: utf-8                 
                      delete_on_start: false            

                    conversation_storage:
                      dirs: ./storage/conversations
                      subdirs: false
                      extension: txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            

                    sets_storage:
                      dirs: ./storage/sets
                      extension: txt
                      subdirs: false
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    maps_storage:
                      dirs: ./storage/maps
                      extension: txt
                      subdirs: false
                      format: text
                      encoding: utf-8                 
                    rdf_storage:
                      dirs: ./storage/rdfs
                      extension: txt
                      subdirs: true
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            

                    denormal_storage:
                      file: ./storage/lookups/denormal.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    normal_storage:
                      file: ./storage/lookups/normal.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    gender_storage:
                      file: ./storage/lookups/gender.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    person_storage:
                      file: ./storage/lookups/person.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    person2_storage:
                      file: ./storage/lookups/person2.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    regex_storage:
                      file: ./storage/lookups/regex.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            

                    properties_storage:
                      file: ./storage/properties.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    defaults_storage:
                      file: ./storage/defaults.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    twitter_storage:
                      dirs: ./storage/twitter
                      extension: txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    spelling_storage:
                      file: ./storage/spelling/corpus.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    license_storage:
                      file: ./storage/licenses/license.keys
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    pattern_nodes_storage:
                      file: ./storage/nodes/pattern_nodes.conf
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    template_nodes_storage:
                      file: ./storage/nodes/template_nodes.conf
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    binaries_storage:
                      file: ./storage/braintree/braintree.bin
                      format: binary
                      encoding: utf-8                 
                      delete_on_start: false            
                    braintree_storage:
                      file: ./storage/braintree/braintree.xml
                      format: xml
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    preprocessors_storage:
                      file: ./storage/processing/preprocessors.conf
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    postprocessors_storage:
                      file: ./storage/processing/postprocessors.conf
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    postquestionprocessors_storage:
                      file: ./storage/processing/postquestionprocessors.conf
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    usergroups_storage:
                      file: ./storage/security/usergroups.yaml
                      format: yaml
                      encoding: utf-8                 
                      delete_on_start: false            

                    oobs_storage:
                      file: ./storage/oobs/callmom.conf
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            

                    triggers_storage:
                      file: ./storage/triggers/triggers.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    services_storage:
                      dirs: ./storage/services
                      subdirs: true
                      extension: yaml
                      format: yaml
                      encoding: utf-8     
                      delete_on_start: false            

                """, ConsoleConfiguration(), ".")

        file_config = yaml.get_section("file")

        config = FileStorageConfiguration()
        config.load_config_section(yaml, file_config, ".")

        self.assert_object_config(config.categories_storage, dirs=["./storage/categories"], extension="aiml", subdirs=True, fileformat="xml", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.learnf_storage, dirs=["./storage/categories/learnf"], extension="aiml", subdirs=False, fileformat="xml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.conversation_storage, dirs=["./storage/conversations"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.sets_storage, dirs=["./storage/sets"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.maps_storage, dirs=["./storage/maps"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.rdf_storage, dirs=["./storage/rdfs"], extension="txt", subdirs=True, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.denormal_storage, file="./storage/lookups/denormal.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.normal_storage, file="./storage/lookups/normal.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.gender_storage, file="./storage/lookups/gender.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.person_storage, file="./storage/lookups/person.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.person2_storage, file="./storage/lookups/person2.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.regex_storage, file="./storage/lookups/regex.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.properties_storage, file="./storage/properties.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.defaults_storage, file="./storage/defaults.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.twitter_storage, dirs=["./storage/twitter"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.spelling_storage, file="./storage/spelling/corpus.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.license_storage, file="./storage/licenses/license.keys", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.pattern_nodes_storage, file="./storage/nodes/pattern_nodes.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.template_nodes_storage, file="./storage/nodes/template_nodes.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.binaries_storage, file="./storage/braintree/braintree.bin", fileformat="binary", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.braintree_storage, file="./storage/braintree/braintree.xml", fileformat="xml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.preprocessors_storage, file="./storage/processing/preprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.postprocessors_storage, file="./storage/processing/postprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.postquestionprocessors_storage, file="./storage/processing/postquestionprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.usergroups_storage, file="./storage/security/usergroups.yaml", fileformat="yaml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.triggers_storage, file="./storage/triggers/triggers.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.oobs_storage, file="./storage/oobs/callmom.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.services_storage, dirs=["./storage/services"], extension="yaml", subdirs=True, fileformat="yaml", encoding="utf-8", delete_on_start=False)

    def test_initialise_without_config(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                files:
                """, ConsoleConfiguration(), ".")

        file_config = yaml.get_section("files")

        config = FileStorageConfiguration()
        config.load_config_section(yaml, file_config, ".")

        tmpdir = FileStorageConfiguration.get_temp_dir()

        self.assert_object_config(config.categories_storage, dirs=[tmpdir + os.sep + "categories"], extension="aiml", subdirs=True, fileformat="xml", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.learnf_storage, dirs=[tmpdir + os.sep + "categories/learnf"], extension="aiml", subdirs=False, fileformat="xml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.conversation_storage, dirs=[tmpdir + os.sep + "conversations"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.sets_storage, dirs=[tmpdir + os.sep + "sets"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.maps_storage, dirs=[tmpdir + os.sep + "maps"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.rdf_storage, dirs=[tmpdir + os.sep + "rdfs"], extension="txt", subdirs=True, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.denormal_storage, file=tmpdir + os.sep + "lookups/denormal.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.normal_storage, file=tmpdir + os.sep + "lookups/normal.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.gender_storage, file=tmpdir + os.sep + "lookups/gender.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.person_storage, file=tmpdir + os.sep + "lookups/person.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.person2_storage, file=tmpdir + os.sep + "lookups/person2.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.regex_storage, file=tmpdir + os.sep + "regex/regex-templates.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.properties_storage, file=tmpdir + os.sep + "properties/properties.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.defaults_storage, file=tmpdir + os.sep + "properties/defaults.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.twitter_storage, dirs=[tmpdir + os.sep + "twitter"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.spelling_storage, file=tmpdir + os.sep + "spelling/corpus.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.license_storage, file=tmpdir + os.sep + "licenses/license.keys", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.pattern_nodes_storage, file=tmpdir + os.sep + "nodes/pattern_nodes.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.template_nodes_storage, file=tmpdir + os.sep + "nodes/template_nodes.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.binaries_storage, file=tmpdir + os.sep + "binaries/binaries.bin", fileformat="binary", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.braintree_storage, file=tmpdir + os.sep + "braintree/braintree.xml", fileformat="xml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.preprocessors_storage, file=tmpdir + os.sep + "processing/preprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.postprocessors_storage, file=tmpdir + os.sep + "processing/postprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.postquestionprocessors_storage, file=tmpdir + os.sep + "processing/postquestionprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.usergroups_storage, file=tmpdir + os.sep + "security/usergroups.yaml", fileformat="yaml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.triggers_storage, file=tmpdir + os.sep + "triggers/triggers.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.oobs_storage, file=tmpdir + os.sep + "oob/callmom.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.services_storage, dirs=[tmpdir + os.sep + "services"], extension="yaml", subdirs=False, fileformat="yaml", encoding="utf-8", delete_on_start=False)

    def test_initialise_without_config_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
                other:
                """, ConsoleConfiguration(), ".")

        file_config = yaml.get_section("files")

        config = FileStorageConfiguration()
        config.load_config_section(yaml, file_config, ".")

        tmpdir = FileStorageConfiguration.get_temp_dir()

        self.assert_object_config(config.categories_storage, dirs=[tmpdir + os.sep + "categories"], extension="aiml", subdirs=True, fileformat="xml", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.learnf_storage, dirs=[tmpdir + os.sep + "categories/learnf"], extension="aiml", subdirs=False, fileformat="xml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.conversation_storage, dirs=[tmpdir + os.sep + "conversations"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.sets_storage, dirs=[tmpdir + os.sep + "sets"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.maps_storage, dirs=[tmpdir + os.sep + "maps"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.rdf_storage, dirs=[tmpdir + os.sep + "rdfs"], extension="txt", subdirs=True, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.denormal_storage, file=tmpdir + os.sep + "lookups/denormal.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.normal_storage, file=tmpdir + os.sep + "lookups/normal.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.gender_storage, file=tmpdir + os.sep + "lookups/gender.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.person_storage, file=tmpdir + os.sep + "lookups/person.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.person2_storage, file=tmpdir + os.sep + "lookups/person2.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.regex_storage, file=tmpdir + os.sep + "regex/regex-templates.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.properties_storage, file=tmpdir + os.sep + "properties/properties.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.defaults_storage, file=tmpdir + os.sep + "properties/defaults.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.twitter_storage, dirs=[tmpdir + os.sep + "twitter"], extension="txt", subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.spelling_storage, file=tmpdir + os.sep + "spelling/corpus.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.license_storage, file=tmpdir + os.sep + "licenses/license.keys", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.pattern_nodes_storage, file=tmpdir + os.sep + "nodes/pattern_nodes.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.template_nodes_storage, file=tmpdir + os.sep + "nodes/template_nodes.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.binaries_storage, file=tmpdir + os.sep + "binaries/binaries.bin", fileformat="binary", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.braintree_storage, file=tmpdir + os.sep + "braintree/braintree.xml", fileformat="xml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.preprocessors_storage, file=tmpdir + os.sep + "processing/preprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.postprocessors_storage, file=tmpdir + os.sep + "processing/postprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        self.assert_object_config(config.postquestionprocessors_storage, file=tmpdir + os.sep + "processing/postquestionprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.usergroups_storage, file=tmpdir + os.sep + "security/usergroups.yaml", fileformat="yaml", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.triggers_storage, file=tmpdir + os.sep + "triggers/triggers.txt", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.oobs_storage, file=tmpdir + os.sep + "oob/callmom.conf", fileformat="text", encoding="utf-8", delete_on_start=False)

        self.assert_object_config(config.services_storage, dirs=[tmpdir + os.sep + "services"], extension="yaml", subdirs=False, fileformat="yaml", encoding="utf-8", delete_on_start=False)

    def assert_object_config(self, config, dirs=None, file=None, extension=None, subdirs=False, fileformat=None, encoding=None, delete_on_start=False):
        self.assertIsNotNone(config)
        if config.has_multiple_dirs() is True:
            self.assertEqual(dirs, config.dirs)
        if config.has_single_file():
            self.assertEqual(file, config.file)
        self.assertEqual(extension, config.extension)
        self.assertEqual(subdirs, config.subdirs)
        self.assertEqual(fileformat, config.format)
        self.assertEqual(encoding, config.encoding)
        self.assertEqual(delete_on_start, config.delete_on_start)

    def _assert_storage_map(self, amap, config):
        self.assertEquals(30, len(amap.keys()))

        self.assertEquals(amap[FileStore.CATEGORIES_STORAGE], config._categories_storage)
        self.assertEquals(amap[FileStore.ERRORS_STORAGE], config._errors_storage)
        self.assertEquals(amap[FileStore.DUPLICATES_STORAGE], config._duplicates_storage)
        self.assertEquals(amap[FileStore.LEARNF_STORAGE], config._learnf_storage)
        self.assertEquals(amap[FileStore.CONVERSATION_STORAGE], config._conversation_storage)
        self.assertEquals(amap[FileStore.SETS_STORAGE], config._sets_storage)
        self.assertEquals(amap[FileStore.MAPS_STORAGE], config._maps_storage)
        self.assertEquals(amap[FileStore.RDF_STORAGE], config._rdf_storage)
        self.assertEquals(amap[FileStore.DENORMAL_STORAGE], config._denormal_storage)
        self.assertEquals(amap[FileStore.NORMAL_STORAGE], config._normal_storage)
        self.assertEquals(amap[FileStore.GENDER_STORAGE], config._gender_storage)
        self.assertEquals(amap[FileStore.PERSON_STORAGE], config._person_storage)
        self.assertEquals(amap[FileStore.PERSON2_STORAGE], config._person2_storage)
        self.assertEquals(amap[FileStore.REGEX_STORAGE], config._regex_storage)
        self.assertEquals(amap[FileStore.PROPERTIES_STORAGE], config._properties_storage)
        self.assertEquals(amap[FileStore.DEFAULTS_STORAGE], config._defaults_storage)
        self.assertEquals(amap[FileStore.TWITTER_STORAGE], config._twitter_storage)
        self.assertEquals(amap[FileStore.SPELLING_STORAGE], config._spelling_storage)
        self.assertEquals(amap[FileStore.LICENSE_STORAGE], config._license_storage)
        self.assertEquals(amap[FileStore.PATTERN_NODES_STORAGE], config._pattern_nodes_storage)
        self.assertEquals(amap[FileStore.TEMPLATE_NODES_STORAGE], config._template_nodes_storage)
        self.assertEquals(amap[FileStore.BINARIES_STORAGE], config._binaries_storage)
        self.assertEquals(amap[FileStore.BRAINTREE_STORAGE], config._braintree_storage)
        self.assertEquals(amap[FileStore.PREPROCESSORS_STORAGE], config._preprocessors_storage)
        self.assertEquals(amap[FileStore.POSTPROCESSORS_STORAGE], config._postprocessors_storage)
        self.assertEquals(amap[FileStore.POSTQUESTIONPROCESSORS_STORAGE], config._postquestionprocessors_storage)
        self.assertEquals(amap[FileStore.USERGROUPS_STORAGE], config._usergroups_storage)
        self.assertEquals(amap[FileStore.TRIGGERS_STORAGE], config._triggers_storage)
        self.assertEquals(amap[FileStore.OOBS_STORAGE], config._oobs_storage)
        self.assertEquals(amap[FileStore.SERVICES_STORAGE], config._services_storage)

    def test_create_storage_map(self):
        amap = {}
        config = FileStorageConfiguration()
        config._create_storage_map(amap)

        self._assert_storage_map(amap, config)

    def test_create_filestorage_config(self):
        config = FileStorageConfiguration()
        amap = config.create_filestorage_config()

        self._assert_storage_map(amap, config)

    def test_to_yaml_with_defaults(self):

        config = FileStorageConfiguration()

        data = {}
        config.to_yaml(data, defaults=True)

        self.assertEquals(30, len(data.keys()))

    def test_to_yaml_no_defaults(self):

        config = FileStorageConfiguration()

        data = {}
        config.to_yaml(data, defaults=False)

        self.assertEquals(30, len(data.keys()))
        self._assert_storage_map(data, config)

    def test_defaults(self):
        filestore_config = FileStorageConfiguration()
        data = {}
        filestore_config.to_yaml(data, True)

        FileStorageConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        tmpdir = FileStorageConfiguration.get_temp_dir()

        FileStorageConfigurationTests.assert_yaml_config(test, data['categories_storage'], dirs=[tmpdir + os.sep + "categories"], extension="aiml",
                                subdirs=True, fileformat="xml", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['learnf_storage'], dirs=[tmpdir + os.sep + "categories/learnf"], extension="aiml",
                                subdirs=False, fileformat="xml", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['conversation_storage'], dirs=[tmpdir + os.sep + "conversations"], extension="txt",
                                subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['sets_storage'], dirs=[tmpdir + os.sep + "sets"], extension="txt", subdirs=False,
                                fileformat="text", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['maps_storage'], dirs=[tmpdir + os.sep + "maps"], extension="txt", subdirs=False,
                                fileformat="text", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['rdf_storage'], dirs=[tmpdir + os.sep + "rdfs"], extension="txt", subdirs=True,
                                fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['denormal_storage'], file=tmpdir + os.sep + "lookups/denormal.txt",
                                fileformat="text", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['normal_storage'], file=tmpdir + os.sep + "lookups/normal.txt", fileformat="text",
                                encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['gender_storage'], file=tmpdir + os.sep + "lookups/gender.txt", fileformat="text",
                                encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['person_storage'], file=tmpdir + os.sep + "lookups/person.txt", fileformat="text",
                                encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['person2_storage'], file=tmpdir + os.sep + "lookups/person2.txt",
                                fileformat="text", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['regex_storage'], file=tmpdir + os.sep + "regex/regex-templates.txt", fileformat="text",
                                encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['properties_storage'], file=tmpdir + os.sep + "properties/properties.txt", fileformat="text",
                                encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['defaults_storage'], file=tmpdir + os.sep + "properties/defaults.txt", fileformat="text",
                                encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['twitter_storage'], dirs=[tmpdir + os.sep + "twitter"], extension="txt",
                                subdirs=False, fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['spelling_storage'], file=tmpdir + os.sep + "spelling/corpus.txt",
                                fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['license_storage'], file=tmpdir + os.sep + "licenses/license.keys",
                                fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['pattern_nodes_storage'], file=tmpdir + os.sep + "nodes/pattern_nodes.conf",
                                fileformat="text", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['template_nodes_storage'], file=tmpdir + os.sep + "nodes/template_nodes.conf",
                                fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['binaries_storage'], file=tmpdir + os.sep + "braintree/braintree.bin",
                                fileformat="binary", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['braintree_storage'], file=tmpdir + os.sep + "braintree/braintree.xml",
                                fileformat="xml", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['preprocessors_storage'], file=tmpdir + os.sep + "processing/preprocessors.conf",
                                fileformat="text", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['postprocessors_storage'], file=tmpdir + os.sep + "processing/postprocessors.conf",
                                fileformat="text", encoding="utf-8", delete_on_start=False)
        FileStorageConfigurationTests.assert_yaml_config(test, data['postquestionprocessors_storage'],
                                file=tmpdir + os.sep + "processing/postquestionprocessors.conf", fileformat="text",
                                encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['usergroups_storage'], file=tmpdir + os.sep + "security/usergroups.yaml",
                                fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['triggers_storage'], file=tmpdir + os.sep + "triggers/triggers.txt",
                                fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['oobs_storage'], file=tmpdir + os.sep + "oobs/callmom.conf",
                                fileformat="text", encoding="utf-8", delete_on_start=False)

        FileStorageConfigurationTests.assert_yaml_config(test, data['services_storage'], dirs=[tmpdir + os.sep + "services"], extension="yaml",
                                subdirs=True, fileformat="yaml", encoding="utf-8", delete_on_start=False)

    @staticmethod
    def assert_yaml_config(test, config, dirs=None, file=None, extension=None, subdirs=False, fileformat=None, encoding=None, delete_on_start=False):
        test.assertIsNotNone(config)

        if dirs is not None:
            test.assertEqual(dirs, config['dirs'])

        if file is not None:
            test.assertEqual(file, config['file'])

        test.assertEqual(extension, config['extension'])
        test.assertEqual(subdirs, config['subdirs'])
        test.assertEqual(fileformat, config['format'])
        test.assertEqual(encoding, config['encoding'])
        test.assertEqual(delete_on_start, config['delete_on_start'])

