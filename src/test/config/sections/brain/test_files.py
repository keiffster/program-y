import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.files import BrainFilesConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainFilesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                aiml:
                    files: $BOT_ROOT/aiml
                    extension: .aiml
                    directories: true
                    errors: $BOT_ROOT/output/y-bot_errors.txt
                    duplicates: $BOT_ROOT/output/y-bot_duplicates.txt
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
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        files_config = BrainFilesConfiguration()
        files_config.load_config_section(yaml, brain_config, ".")

        self.assertIsNotNone(files_config.aiml_files)
        self.assertEqual("./aiml", files_config.aiml_files.files)
        self.assertEqual(".aiml", files_config.aiml_files.extension)
        self.assertTrue(files_config.aiml_files.directories)
        self.assertEqual("./output/y-bot_errors.txt", files_config.aiml_files.errors)
        self.assertEqual("./output/y-bot_duplicates.txt", files_config.aiml_files.duplicates)

        self.assertIsNotNone(files_config.set_files)
        self.assertEqual("./sets", files_config.set_files.files)
        self.assertEqual(".txt", files_config.set_files.extension)
        self.assertFalse(files_config.set_files.directories)

        self.assertIsNotNone(files_config.map_files)
        self.assertEqual("./maps", files_config.map_files.files)
        self.assertEqual(".txt", files_config.map_files.extension)
        self.assertFalse(files_config.map_files.directories)

        self.assertEqual(files_config.denormal, "./config/denormal.txt")
        self.assertEqual(files_config.normal, "./config/normal.txt")
        self.assertEqual(files_config.gender, "./config/gender.txt")
        self.assertEqual(files_config.person, "./config/person.txt")
        self.assertEqual(files_config.person2, "./config/person2.txt")
        self.assertEqual(files_config.predicates, "./config/predicates.txt")
        self.assertEqual(files_config.pronouns, "./config/pronouns.txt")
        self.assertEqual(files_config.properties, "./config/properties.txt")
        self.assertEqual(files_config.triples, "./config/triples.txt")
        self.assertEqual(files_config.preprocessors, "./config/preprocessors.conf")
        self.assertEqual(files_config.postprocessors, "./config/postprocessors.conf")
