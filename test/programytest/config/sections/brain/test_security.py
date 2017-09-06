import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.security import BrainSecurityConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainSecurityConfigurationTests(unittest.TestCase):

    def test_authorisation_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authorisation:
                    classname: programy.utils.security.authorise.passthrough.PassThroughAuthorisationService
                    denied_srai: AUTHORISATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authorisation")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.utils.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual("AUTHORISATION_FAILED", service_config.denied_srai)

    def test_authentication_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.utils.security.authenticate.passthrough.PassThroughAuthenticationService
                    denied_srai: AUTHENTICATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authentication")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.utils.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual("AUTHENTICATION_FAILED", service_config.denied_srai)
