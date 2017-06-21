import unittest

from programy.config.brain import BrainFileConfiguration
from programy.config.brain import BrainServiceConfiguration
from programy.config.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration


class BrainFileConfigurationTests(unittest.TestCase):

    def test_init_defaults(self):
        file_config = BrainFileConfiguration(files="/aiml")
        self.assertEqual(file_config.files, "/aiml")
        self.assertEqual(file_config.extension, ".aiml")
        self.assertEqual(file_config.directories, False)

    def test_init(self):
        file_config = BrainFileConfiguration(files="/aiml", extension=".txt", directories=True)
        self.assertEqual(file_config.files, "/aiml")
        self.assertEqual(file_config.extension, ".txt")
        self.assertEqual(file_config.directories, True)



class BrainServiceConfigurationTests(unittest.TestCase):

    def test_init_default(self):
        service_config = BrainServiceConfiguration("Rest")
        self.assertEqual(service_config.name, "REST")
        self.assertEqual(len(service_config.parameters()), 0)

    def test_init(self):
        service_config = BrainServiceConfiguration("REST", {"path": "com.keithsterling.object", "debug": True})
        self.assertEqual(service_config.name, "REST")
        self.assertEqual(len(service_config.parameters()), 2)
        self.assertEqual(service_config.parameter("PATH"), "com.keithsterling.object")
        self.assertEqual(service_config.parameter("DEBUG"), True)
        self.assertEqual(service_config.parameter("XXXX"), None)


class BrainConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
          supress_warnings: true
          allow_system_aiml: true
          allow_learn_aiml: true
          allow_learnf_aiml: true
          dump_to_file: /tmp/braintree.txt

          files:
                aiml:

                    files: $BOT_ROOT/aiml
                    extension: .aiml
                    directories: false
                sets:
                    files: $BOT_ROOT/sets
                    extension: .txt
                    directories: false
                maps:
                    files: $BOT_ROOT/maps
                    extension: .txt
                    directories: false
                denormal: $BOT_ROOT/config/denormal.txt
                normal: $BOT_ROOT/config/normal.txt
                gender: $BOT_ROOT/config/gender.txt
                person: $BOT_ROOT/config/person.txt
                person2: $BOT_ROOT/config/person2.txt
                predicates: $BOT_ROOT/config/predicates.txt
                pronouns: $BOT_ROOT/config/pronouns.txt
                properties: $BOT_ROOT/config/properties.txt
                triples: $BOT_ROOT/config/triples.txt
                preprocessors: $BOT_ROOT/config/preprocessors.conf
                postprocessors: $BOT_ROOT/config/postprocessors.conf

        """, ".")

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        self.assertEqual(True, brain_config.allow_system_aiml)
        self.assertEqual(True, brain_config.allow_learn_aiml)
        self.assertEqual(True, brain_config.allow_learnf_aiml)
        self.assertEqual("/tmp/braintree.txt", brain_config.dump_to_file)
        self.assertIsNotNone(brain_config.aiml_files)
        self.assertIsNotNone(brain_config.set_files)
        self.assertIsNotNone(brain_config.map_files)
        self.assertEqual("./config/denormal.txt", brain_config.denormal)
        self.assertEqual("./config/normal.txt", brain_config.normal)
        self.assertEqual("./config/gender.txt", brain_config.gender)
        self.assertEqual("./config/person.txt", brain_config.person)
        self.assertEqual("./config/person2.txt", brain_config.person2)
        self.assertEqual("./config/predicates.txt", brain_config.predicates)
        self.assertEqual("./config/pronouns.txt", brain_config.pronouns)
        self.assertEqual("./config/properties.txt", brain_config.properties)
        self.assertEqual("./config/triples.txt", brain_config.triples)
        self.assertEqual("./config/preprocessors.conf", brain_config.preprocessors)
        self.assertEqual("./config/postprocessors.conf", brain_config.postprocessors)
        self.assertIsNotNone(brain_config.services)

