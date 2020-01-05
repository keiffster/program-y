import unittest
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.config.brain.security import BrainSecurityAccountLinkerConfiguration

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

        service_config = BrainSecurityAuthorisationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual("AUTHORISATION_FAILED", service_config.denied_srai)
        self.assertEqual(BrainSecurityAuthorisationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)

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

        service_config = BrainSecurityAuthorisationConfiguration()
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

        service_config = BrainSecurityAuthorisationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual(BrainSecurityAuthorisationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
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

        service_config = BrainSecurityAuthenticationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual("AUTHENTICATION_FAILED", service_config.denied_srai)
        self.assertEqual(BrainSecurityAuthenticationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)

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

        service_config = BrainSecurityAuthenticationConfiguration()
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

        service_config = BrainSecurityAuthenticationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual(BrainSecurityAuthenticationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
        self.assertEqual(BrainSecurityAuthenticationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)

    def test_defaults(self):
        authenticate_config = BrainSecurityAuthenticationConfiguration()
        data = {}
        authenticate_config.to_yaml(data, True)

        BrainSecurityConfigurationTests.assert_authenticate_defaults(self, data)

        authorise_config = BrainSecurityAuthorisationConfiguration()
        data = {}
        authorise_config.to_yaml(data, True)

        BrainSecurityConfigurationTests.assert_authorise_defaults(self, data)

        accountlinker_config = BrainSecurityAccountLinkerConfiguration()
        data = {}
        accountlinker_config.to_yaml(data, True)

        BrainSecurityConfigurationTests.assert_accountlinker_defaults(self, data)

    @staticmethod
    def assert_authenticate_defaults(test, data):
        test.assertEqual(data['classname'], "programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService")
        test.assertEqual(data['denied_srai'], "AUTHENTICATION_FAILED")
        test.assertEqual(data['denied_text'], "Access Denied!")

    @staticmethod
    def assert_authorise_defaults(test, data):
        test.assertEqual(data['classname'], "programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService")
        test.assertEqual(data['denied_srai'], "AUTHORISATION_FAILED")
        test.assertEqual(data['denied_text'], "Access Denied!")

    @staticmethod
    def assert_accountlinker_defaults(test, data):
        test.assertEqual(data['classname'], "programy.security.linking.accountlinker.BasicAccountLinkerService")
        test.assertEqual(data['denied_srai'], "ACCOUNT_LINKING_FAILED")
        test.assertEqual(data['denied_text'], "Unable to link accounts!")
