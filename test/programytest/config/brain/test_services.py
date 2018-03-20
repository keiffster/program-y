import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.services import BrainServicesConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainServicesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
                REST:
                    classname: programy.services.rest.GenericRESTService
                    method: GET
                    host: 0.0.0.0
                Pannous:
                    classname: programy.services.pannous.PannousService
                    url: http://weannie.pannous.com/api
                Pandora:
                    classname: programy.services.pandora.PandoraService
                    url: http://www.pandorabots.com/pandora/talk-xml
                Wikipedia:
                    classname: programy.services.wikipediaservice.WikipediaService
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        services_config = BrainServicesConfiguration()
        services_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(services_config.exists("REST"))
        self.assertTrue(services_config.exists("Pannous"))
        self.assertTrue(services_config.exists("Pandora"))
        self.assertTrue(services_config.exists("Wikipedia"))
        self.assertFalse(services_config.exists("Other"))

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            services:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        services_config = BrainServicesConfiguration()
        services_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(services_config.exists("REST"))
        self.assertFalse(services_config.exists("Pannous"))
        self.assertFalse(services_config.exists("Pandora"))
        self.assertFalse(services_config.exists("Wikipedia"))
        self.assertFalse(services_config.exists("Other"))

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        services_config = BrainServicesConfiguration()
        services_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(services_config.exists("REST"))
        self.assertFalse(services_config.exists("Pannous"))
        self.assertFalse(services_config.exists("Pandora"))
        self.assertFalse(services_config.exists("Wikipedia"))
        self.assertFalse(services_config.exists("Other"))
