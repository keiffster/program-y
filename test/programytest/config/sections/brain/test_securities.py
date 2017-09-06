import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.securities import BrainSecuritiesConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainSecuritiesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.utils.security.authenticate.passthrough.PassThroughAuthenticationService
                    denied_srai: AUTHENTICATION_FAILED
                authorisation:
                    classname: programy.utils.security.authorise.passthrough.PassThroughAuthorisationService
                    denied_srai: AUTHORISATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        securities_config = BrainSecuritiesConfiguration()
        securities_config.load_config_section(yaml, brain_config, ".")

        self.assertIsNotNone(securities_config.authorisation)
        self.assertIsNotNone(securities_config.authentication)