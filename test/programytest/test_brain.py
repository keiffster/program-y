import os
import unittest
from unittest.mock import patch
from programy.brain import Brain
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.oob.default import DefaultOutOfBandProcessor
from programytest.client import TestClient


class BrainTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def load_os_specific_configuration(self, yaml, linux_filename, windows_filename):
        if os.name == 'posix':
            yaml.load_from_file(os.path.dirname(__file__)+ os.sep + "testdata" + os.sep + linux_filename, ConsoleConfiguration(), os.path.dirname(__file__))
        elif os.name == 'nt':
            yaml.load_from_file(os.path.dirname(__file__)+ os.sep + "testdata" + os.sep + windows_filename, ConsoleConfiguration(), os.path.dirname(__file__))
        else:
            raise Exception("Unknown os [%s]"%os.name)

    def test_brain_init_no_config(self):
        client = TestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain)

        self.assertIsNotNone(client_context.brain.aiml_parser)
        self.assertIsNotNone(client_context.brain.denormals)
        self.assertIsNotNone(client_context.brain.normals)
        self.assertIsNotNone(client_context.brain.genders)
        self.assertIsNotNone(client_context.brain.persons)
        self.assertIsNotNone(client_context.brain.person2s)
        self.assertIsNotNone(client_context.brain.properties)
        self.assertIsNotNone(client_context.brain.rdf)
        self.assertIsNotNone(client_context.brain.sets)
        self.assertIsNotNone(client_context.brain.maps)
        self.assertIsNotNone(client_context.brain.preprocessors)
        self.assertIsNotNone(client_context.brain.postprocessors)
        self.assertIsNotNone(client_context.brain.security)

    def test_brain_init_with_config(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brains_section = yaml.get_section("brains")
        brain_section = yaml.get_section("brain", brains_section)

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, brain_section, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain)

        self.assertIsNotNone(brain.aiml_parser)
        self.assertIsNotNone(brain.denormals)
        self.assertIsNotNone(brain.normals)
        self.assertIsNotNone(brain.genders)
        self.assertIsNotNone(brain.persons)
        self.assertIsNotNone(brain.person2s)
        self.assertIsNotNone(brain.properties)
        self.assertIsNotNone(brain.rdf)
        self.assertIsNotNone(brain.sets)
        self.assertIsNotNone(brain.maps)
        self.assertIsNotNone(brain.preprocessors)
        self.assertIsNotNone(brain.postprocessors)
        self.assertIsNotNone(brain.security)

    def test_brain_init_with_secure_config(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_secure_brain.yaml", "test_secure_brain.windows.yaml")

        brains_section = yaml.get_section("brains")
        brain_section = yaml.get_section("brain", brains_section)

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, brain_section, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain)

        self.assertIsNotNone(brain.aiml_parser)
        self.assertIsNotNone(brain.denormals)
        self.assertIsNotNone(brain.normals)
        self.assertIsNotNone(brain.genders)
        self.assertIsNotNone(brain.persons)
        self.assertIsNotNone(brain.person2s)
        self.assertIsNotNone(brain.properties)
        self.assertIsNotNone(brain.rdf)
        self.assertIsNotNone(brain.sets)
        self.assertIsNotNone(brain.maps)
        self.assertIsNotNone(brain.preprocessors)
        self.assertIsNotNone(brain.postprocessors)
        self.assertIsNotNone(brain.security)

    def test_oob_loading(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brains_section = yaml.get_section("brains")
        brain_section = yaml.get_section("brain", brains_section)

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, brain_section, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        self.assertIsInstance(brain._oobhandler.default_oob, DefaultOutOfBandProcessor)

    def test_reload_unknowns(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brains_section = yaml.get_section("brains")
        brain_section = yaml.get_section("brain", brains_section)

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, brain_section, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        brain.reload_map("Unknown")
        brain.reload_set("Unknown")
        brain.reload_rdf("Unknown")

    def test_load_save_binaries(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_secure_brain.yaml", "test_secure_brain.windows.yaml")

        brains_section = yaml.get_section("brains")
        brain_section = yaml.get_section("brain", brains_section)

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, brain_section, ".")

        brain_config.binaries._save_binary = True
        brain_config.binaries._load_binary = False

        client = TestClient()
        client_context = client.create_client_context("testid")

        brain1 = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain1)

        brain_config.binaries._save_binary = False
        brain_config.binaries._load_binary = True

        brain2 = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain2)

    def test_post_process_question_no_processing(self):
        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brains_section = yaml.get_section("brains")
        brain_section = yaml.get_section("brain", brains_section)

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, brain_section, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain)

        response = brain.post_process_question(client_context, "Hello")
        self.assertIsNone(response)

    def patch_process(self, client_context, question):
        return "Other"

    @patch("programy.processors.processing.ProcessorCollection.process", patch_process)
    def test_post_process_question_with_processing(self):
        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brains_section = yaml.get_section("brains")
        brain_section = yaml.get_section("brain", brains_section)

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, brain_section, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain)

        response = brain.post_process_question(client_context, "Hello")
        self.assertEquals("Other", response)
