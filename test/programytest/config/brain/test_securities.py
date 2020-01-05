import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.securities import BrainSecuritiesConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programytest.config.brain.test_security import BrainSecurityConfigurationTests


class BrainSecuritiesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
                    denied_srai: AUTHENTICATION_FAILED
                authorisation:
                    classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
                    denied_srai: AUTHORISATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        securities_config = BrainSecuritiesConfiguration()
        securities_config.load_config_section(yaml, brain_config, ".")

        self.assertIsNotNone(securities_config.authorisation)
        self.assertIsNotNone(securities_config.authentication)

    def test_defaults(self):
        securities_config = BrainSecuritiesConfiguration()
        data = {}
        securities_config.to_yaml(data, True)

    @staticmethod
    def assert_defaults(test, data):
        BrainSecurityConfigurationTests.assert_authenticate_defaults(test, data['authentication'])
        BrainSecurityConfigurationTests.assert_authorise_defaults(test, data['authorisation'])
        BrainSecurityConfigurationTests.assert_accountlinker_defaults(test, data['account_linker'])
