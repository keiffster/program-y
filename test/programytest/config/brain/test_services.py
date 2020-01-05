import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.services import BrainServicesConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


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

        self.assertIsNotNone(services_config.service("REST"))
        self.assertIsNone(services_config.service("REST2"))

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

    def test_defaults(self):
        services_config = BrainServicesConfiguration()
        data = {}
        services_config.to_yaml(data, True)

        BrainServicesConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEquals(data['REST']['classname'], 'programy.services.rest.GenericRESTService')
        test.assertEquals(data['REST']['method'], 'GET')
        test.assertEquals(data['REST']['host'], '0.0.0.0')

        test.assertEquals(data['Pannous']['classname'], 'programy.services.pannous.PannousService')
        test.assertEquals(data['Pannous']['url'], 'http://weannie.pannous.com/api')

        test.assertEquals(data['Pandora']['classname'], 'programy.services.pandora.PandoraService')
        test.assertEquals(data['Pandora']['url'], 'http://www.pandorabots.com/pandora/talk-xml')

        test.assertEquals(data['Wikipedia']['classname'], 'programy.services.wikipediaservice.WikipediaService')

        test.assertEquals(data['DuckDuckGo']['classname'], 'programy.services.duckduckgo.DuckDuckGoService')
        test.assertEquals(data['DuckDuckGo']['url'], 'http://api.duckduckgo.com')
