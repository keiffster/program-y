import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.security import BrainSecurityConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainSecurityConfigurationTests(unittest.TestCase):

    def test_authorisation_with_data_denied_srai(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authorisation:
                    classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
                    denied_srai: AUTHORISATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authorisation")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual("AUTHORISATION_FAILED", service_config.denied_srai)
        self.assertEqual(BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)

    def test_authorisation_with_data_denied_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authorisation:
                    classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
                    denied_text: Authorisation Failed
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authorisation")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual("Authorisation Failed", service_config.denied_text)
        self.assertIsNone(service_config.denied_srai)

    def test_authorisation_with_data_neither_denied_srai_or_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authorisation:
                    classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authorisation")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual(BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
        self.assertIsNone(service_config.denied_srai)

    def test_authentication_with_data_denied_srai(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
                    denied_srai: AUTHENTICATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authentication")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual("AUTHENTICATION_FAILED", service_config.denied_srai)
        self.assertEqual(BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)

    def test_authentication_with_data_denied_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
                    denied_text: Authentication failed
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authentication")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual("Authentication failed", service_config.denied_text)
        self.assertIsNone(service_config.denied_srai)

    def test_authentication_with_data_neither_denied_srai_or_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityConfiguration("authentication")
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual(BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
        self.assertEqual(BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
