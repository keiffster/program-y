import unittest
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.license.keys import LicenseKeys
from programytest.config.brain.test_braintree import BrainBraintreeConfigurationTests
from programytest.config.brain.test_binaries import BrainBinariesConfigurationTests
from programytest.config.brain.test_debugfiles import BrainDebugFilesConfigurationTests
from programytest.config.brain.test_defaults import BrainDefaultsDefaultsConfigurationTests
from programytest.config.brain.test_dynamic import BrainDynamicsConfigurationTests
from programytest.config.brain.test_overrides import BrainOverridesConfigurationTests
from programytest.config.brain.test_securities import BrainSecuritiesConfigurationTests
from programytest.config.brain.test_tokenizer import BrainTokenizerConfigurationTests


class BrainConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
brain:

    # Overrides
    overrides:
      allow_system_aiml: true
      allow_learn_aiml: true
      allow_learnf_aiml: true

    # Defaults
    defaults:
      default_get: unknown
      default_property: unknown
      default_map: unknown
      learnf_path: file

    # Binary
    binaries:
      save_binary: true
      load_binary: true
      load_aiml_on_binary_fail: true

    # Braintree
    braintree:
      create: true

    security:
        authentication:
            classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
            denied_srai: AUTHENTICATION_FAILED
        authorisation:
            classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
            denied_srai: AUTHORISATION_FAILED
            usergroups:
              storage: file

    dynamic:
        variables:
            gettime: programy.dynamic.variables.datetime.GetTime
        sets:
            numeric: programy.dynamic.sets.numeric.IsNumeric
            roman:   programy.dynamic.sets.roman.IsRomanNumeral
        maps:
            romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
            dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman

        """, ConsoleConfiguration(), ".")

        brain_section = yaml.get_section("brain")

        brain_configuration = BrainConfiguration()
        brain_configuration.load_configuration(yaml, brain_section, ".")

        BrainConfigurationTests.assert_brain_config(self, brain_configuration)

    @staticmethod
    def assert_brain_config(test, brain_configuration):
        test.assertTrue(brain_configuration.overrides.allow_system_aiml)
        test.assertTrue(brain_configuration.overrides.allow_learn_aiml)
        test.assertTrue(brain_configuration.overrides.allow_learnf_aiml)

        test.assertIsNotNone(brain_configuration.defaults)
        test.assertEqual(brain_configuration.defaults.default_get, "unknown")
        test.assertEqual(brain_configuration.defaults.default_property, "unknown")
        test.assertEqual(brain_configuration.defaults.default_map, "unknown")

        test.assertIsNotNone(brain_configuration.binaries)
        test.assertTrue(brain_configuration.binaries.save_binary)
        test.assertTrue(brain_configuration.binaries.load_binary)
        test.assertTrue(brain_configuration.binaries.load_aiml_on_binary_fail)

        test.assertIsNotNone(brain_configuration.braintree)
        test.assertTrue(brain_configuration.braintree.create)

        test.assertIsNotNone(brain_configuration.security)
        test.assertIsNotNone(brain_configuration.security.authorisation)
        test.assertIsNotNone(brain_configuration.security.authentication)

        test.assertIsNotNone(brain_configuration.dynamics)
        test.assertIsNotNone(brain_configuration.dynamics.dynamic_sets)

        test.assertIsNotNone(brain_configuration.dynamics.dynamic_maps)
        test.assertIsNotNone(brain_configuration.dynamics.dynamic_vars)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        brain_configuration = BrainConfiguration()
        brain_configuration.load_configuration(yaml, brain_config, ".")

        self.assertFalse(brain_configuration.overrides.allow_system_aiml)
        self.assertFalse(brain_configuration.overrides.allow_learn_aiml)
        self.assertFalse(brain_configuration.overrides.allow_learnf_aiml)

        self.assertIsNotNone(brain_configuration.defaults)
        self.assertEqual(brain_configuration.defaults.default_get, "unknown")
        self.assertEqual(brain_configuration.defaults.default_property, "unknown")
        self.assertEqual(brain_configuration.defaults.default_map, "unknown")

        self.assertIsNotNone(brain_configuration.binaries)
        self.assertFalse(brain_configuration.binaries.save_binary)
        self.assertFalse(brain_configuration.binaries.load_binary)
        self.assertFalse(brain_configuration.binaries.load_aiml_on_binary_fail)

        self.assertIsNotNone(brain_configuration.braintree)
        self.assertFalse(brain_configuration.braintree.create)

        self.assertIsNotNone(brain_configuration.security)
        self.assertIsNone(brain_configuration.security.authorisation)
        self.assertIsNone(brain_configuration.security.authentication)

        self.assertIsNotNone(brain_configuration.dynamics)
        self.assertIsNotNone(brain_configuration.dynamics.dynamic_sets)

        self.assertIsNotNone(brain_configuration.dynamics.dynamic_maps)
        self.assertIsNotNone(brain_configuration.dynamics.dynamic_vars)

    def test_check_for_license_keys(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
               """, ConsoleConfiguration(), ".")

        brain_section = yaml.get_section("brain")

        brain_configuration = BrainConfiguration()
        brain_configuration.load_configuration(yaml, brain_section, ".")

        license_keys = LicenseKeys()

        brain_configuration.check_for_license_keys(license_keys)

    def test_defaults(self):
        brain_configuration = BrainConfiguration()
        data = {}
        brain_configuration.to_yaml(data, True)

        BrainConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertTrue('braintree' in data)
        BrainBraintreeConfigurationTests.assert_defaults(test, data['braintree'])
        test.assertTrue('binaries' in data)
        BrainBinariesConfigurationTests.assert_defaults(test, data['binaries'])
        test.assertTrue('debugfiles' in data)
        BrainDebugFilesConfigurationTests.assert_defaults(test, data['debugfiles'])
        test.assertTrue('defaults' in data)
        BrainDefaultsDefaultsConfigurationTests.assert_defaults(test, data['defaults'])
        test.assertTrue('dynamic' in data)
        BrainDynamicsConfigurationTests.assert_defaults(test, data['dynamic'])
        test.assertTrue('overrides' in data)
        BrainOverridesConfigurationTests.assert_defaults(test, data['overrides'])
        test.assertTrue('security' in data)
        BrainSecuritiesConfigurationTests.assert_defaults(test, data['security'])
        test.assertTrue('tokenizer' in data)
        BrainTokenizerConfigurationTests.assert_defaults(test, data['tokenizer'])