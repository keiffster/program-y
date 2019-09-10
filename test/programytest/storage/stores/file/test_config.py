import unittest
import os

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

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
                    variables_storage:
                      dirs: ./storage/variables
                      extension: txt
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
                      file: ./storage/nodes/pattern_nodes.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    template_nodes_storage:
                      file: ./storage/nodes/template_nodes.txt
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
                      file: ./storage/processing/preprocessors.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                    postprocessors_storage:
                      file: ./storage/processing/postprocessors.txt
                      format: text
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                    usergroups_storage:
                      file: ./storage/security/usergroups.yaml
                      format: yaml
                      encoding: utf-8                 
                      delete_on_start: false            
                      
                """, ConsoleConfiguration(), ".")

        file_config = yaml.get_section("file")

        config = FileStorageConfiguration()
        config.load_config_section(yaml, file_config, ".")

        self.assert_config(config.categories_storage, dirs=["./storage/categories"], extension="aiml", subdirs=True, format="xml", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.learnf_storage, dirs=["./storage/categories/learnf"], extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.conversation_storage, dirs=["./storage/conversations"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.sets_storage, dirs=["./storage/sets"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.maps_storage, dirs=["./storage/maps"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.rdf_storage, dirs=["./storage/rdfs"], extension="txt", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.denormal_storage, file="./storage/lookups/denormal.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.normal_storage, file="./storage/lookups/normal.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.gender_storage, file="./storage/lookups/gender.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.person_storage, file="./storage/lookups/person.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.person2_storage, file="./storage/lookups/person2.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.regex_storage, file="./storage/lookups/regex.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.properties_storage, file="./storage/properties.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.defaults_storage, file="./storage/defaults.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.twitter_storage, dirs=["./storage/twitter"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.spelling_storage, file="./storage/spelling/corpus.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.license_storage, file="./storage/licenses/license.keys", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.pattern_nodes_storage, file="./storage/nodes/pattern_nodes.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.template_nodes_storage, file="./storage/nodes/template_nodes.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.binaries_storage, file="./storage/braintree/braintree.bin", format="binary", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.braintree_storage, file="./storage/braintree/braintree.xml", format="xml", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.preprocessors_storage, file="./storage/processing/preprocessors.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.postprocessors_storage, file="./storage/processing/postprocessors.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.usergroups_storage, file="./storage/security/usergroups.yaml", format="yaml", encoding="utf-8", delete_on_start=False)

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

        self.assert_config(config.categories_storage, dirs=[tmpdir + os.sep + "categories"], extension="aiml", subdirs=True, format="xml", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.learnf_storage, dirs=[tmpdir + os.sep + "categories/learnf"], extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.conversation_storage, dirs=[tmpdir + os.sep + "conversations"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.sets_storage, dirs=[tmpdir + os.sep + "sets"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.maps_storage, dirs=[tmpdir + os.sep + "maps"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.rdf_storage, dirs=[tmpdir + os.sep + "rdfs"], extension="txt", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.denormal_storage, file=tmpdir + os.sep + "lookups/denormal.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.normal_storage, file=tmpdir + os.sep + "lookups/normal.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.gender_storage, file=tmpdir + os.sep + "lookups/gender.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.person_storage, file=tmpdir + os.sep + "lookups/person.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.person2_storage, file=tmpdir + os.sep + "lookups/person2.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.regex_storage, file=tmpdir + os.sep + "lookups/regex.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.properties_storage, file=tmpdir + os.sep + "properties.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.defaults_storage, file=tmpdir + os.sep + "defaults.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.twitter_storage, dirs=[tmpdir + os.sep + "twitter"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.spelling_storage, file=tmpdir + os.sep + "spelling/corpus.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.license_storage, file=tmpdir + os.sep + "licenses/license.keys", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.pattern_nodes_storage, file=tmpdir + os.sep + "nodes/pattern_nodes.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.template_nodes_storage, file=tmpdir + os.sep + "nodes/template_nodes.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.binaries_storage, file=tmpdir + os.sep + "braintree/braintree.bin", format="binary", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.braintree_storage, file=tmpdir + os.sep + "braintree/braintree.xml", format="xml", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.preprocessors_storage, file=tmpdir + os.sep + "processing/preprocessors.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(config.postprocessors_storage, file=tmpdir + os.sep + "processing/postprocessors.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(config.usergroups_storage, file=tmpdir + os.sep + "security/usergroups.yaml", format="yaml", encoding="utf-8", delete_on_start=False)

    def test_create_storage_defaults(self):
        amap = {}

        config = FileStorageConfiguration()
        config._create_storage_defaults(amap)

        tmpdir = FileStorageConfiguration.get_temp_dir()

        self.assert_config(amap['categories_storage'], dirs=[tmpdir + os.sep + "categories"], extension="aiml", subdirs=True, format="xml", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['learnf_storage'], dirs=[tmpdir + os.sep + "categories/learnf"], extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['conversation_storage'], dirs=[tmpdir + os.sep + "conversations"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['sets_storage'], dirs=[tmpdir + os.sep + "sets"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['maps_storage'], dirs=[tmpdir + os.sep + "maps"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['rdf_storage'], dirs=[tmpdir + os.sep + "rdfs"], extension="txt", subdirs=True, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['denormal_storage'], file=tmpdir + os.sep + "lookups/denormal.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['normal_storage'], file=tmpdir + os.sep + "lookups/normal.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['gender_storage'], file=tmpdir + os.sep + "lookups/gender.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['person_storage'], file=tmpdir + os.sep + "lookups/person.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['person2_storage'], file=tmpdir + os.sep + "lookups/person2.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['regex_storage'], file=tmpdir + os.sep + "lookups/regex.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['properties_storage'], file=tmpdir + os.sep + "properties.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['defaults_storage'], file=tmpdir + os.sep + "defaults.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['variables_storage'], dirs=[tmpdir + os.sep + "variables"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['twitter_storage'], dirs=[tmpdir + os.sep + "twitter"], extension="txt", subdirs=False, format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['spelling_storage'], file=tmpdir + os.sep + "spelling/corpus.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['license_storage'], file=tmpdir + os.sep + "licenses/license.keys", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['pattern_nodes_storage'], file=tmpdir + os.sep + "nodes/pattern_nodes.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['template_nodes_storage'], file=tmpdir + os.sep + "nodes/template_nodes.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['binaries_storage'], file=tmpdir + os.sep + "braintree/braintree.bin", format="binary", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['braintree_storage'], file=tmpdir + os.sep + "braintree/braintree.xml", format="xml", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['preprocessors_storage'], file=tmpdir + os.sep + "processing/preprocessors.txt", format="text", encoding="utf-8", delete_on_start=False)
        self.assert_config(amap['postprocessors_storage'], file=tmpdir + os.sep + "processing/postprocessors.txt", format="text", encoding="utf-8", delete_on_start=False)

        self.assert_config(amap['usergroups_storage'], file=tmpdir + os.sep + "security/usergroups.txt", format="text", encoding="utf-8", delete_on_start=False)

    def assert_config(self, config, dirs=None, file=None, extension=None, subdirs=False, format=None, encoding=None, delete_on_start=False):
        self.assertIsNotNone(config)
        if config.has_multiple_dirs() is True:
            self.assertEqual(dirs, config.dirs)
        if config.has_single_file():
            self.assertEqual(file, config.file)
        self.assertEqual(extension, config.extension)
        self.assertEqual(subdirs, config.subdirs)
        self.assertEqual(format, config.format)
        self.assertEqual(encoding, config.encoding)
        self.assertEqual(delete_on_start, config.delete_on_start)
