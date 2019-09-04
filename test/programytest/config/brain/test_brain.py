import unittest

from programy.config.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration


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
      default-get: unknown
      default-property: unknown
      default-map: unknown
      learnf-path: file

    # Binary
    binaries:
      save_binary: true
      load_binary: true
      load_aiml_on_binary_fail: true

    # Braintree
    braintree:
      create: true

    services:
        OPENCHAT:
            classname: programy.services.openchat.openchat.service.OpenChatRESTService
        REST:
            classname: programy.services.rest.GenericRESTService
            method: GET
            host: 0.0.0.0
            port: 8080
        Pannous:
            classname: programy.services.pannous.PannousService
            url: http://weannie.pannous.com/api

    openchatbots:
      chatbot1:
        url: http://localhost:5959/api/rest/v2.0/ask
        method: GET

    security:
        authentication:
            classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
            denied_srai: AUTHENTICATION_FAILED
        authorisation:
            classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
            denied_srai: AUTHORISATION_FAILED
            usergroups:
              storage: file

    oob:
      default:
        classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
      alarm:
        classname: programy.oob.defaults.alarm.AlarmOutOfBandProcessor
      camera:
        classname: programy.oob.defaults.camera.CameraOutOfBandProcessor
      clear:
        classname: programy.oob.defaults.clear.ClearOutOfBandProcessor
      dial:
        classname: programy.oob.defaults.dial.DialOutOfBandProcessor
      dialog:
        classname: programy.oob.defaults.dialog.DialogOutOfBandProcessor
      email:
        classname: programy.oob.defaults.email.EmailOutOfBandProcessor
      geomap:
        classname: programy.oob.defaults.map.MapOutOfBandProcessor
      schedule:
        classname: programy.oob.defaults.schedule.ScheduleOutOfBandProcessor
      search:
        classname: programy.oob.defaults.search.SearchOutOfBandProcessor
      sms:
        classname: programy.oob.defaults.sms.SMSOutOfBandProcessor
      url:
        classname: programy.oob.defaults.url.URLOutOfBandProcessor
      wifi:
        classname: programy.oob.defaults.wifi.WifiOutOfBandProcessor

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

        brain_configuration = BrainConfiguration()
        brain_configuration.load_configuration(yaml, ".")

        self.assertTrue(brain_configuration.overrides.allow_system_aiml)
        self.assertTrue(brain_configuration.overrides.allow_learn_aiml)
        self.assertTrue(brain_configuration.overrides.allow_learnf_aiml)

        self.assertIsNotNone(brain_configuration.defaults)
        self.assertEqual(brain_configuration.defaults.default_get, "unknown")
        self.assertEqual(brain_configuration.defaults.default_property, "unknown")
        self.assertEqual(brain_configuration.defaults.default_map, "unknown")

        self.assertIsNotNone(brain_configuration.binaries)
        self.assertTrue(brain_configuration.binaries.save_binary)
        self.assertTrue(brain_configuration.binaries.load_binary)
        self.assertTrue(brain_configuration.binaries.load_aiml_on_binary_fail)

        self.assertIsNotNone(brain_configuration.braintree)
        self.assertTrue(brain_configuration.braintree.create)

        self.assertIsNotNone(brain_configuration.services)

        self.assertTrue(brain_configuration.services.exists('OPENCHAT'))
        rest_config = brain_configuration.services.service('OPENCHAT')
        self.assertEqual("programy.services.openchat.openchat.service.OpenChatRESTService", rest_config.classname)

        self.assertTrue(brain_configuration.services.exists('REST'))
        rest_config =brain_configuration.services.service('REST')
        self.assertEqual("programy.services.rest.GenericRESTService", rest_config.classname)
        self.assertEqual(rest_config.method, "GET")
        self.assertEqual(rest_config.host, "0.0.0.0")
        self.assertEqual(rest_config.port, 8080)

        pannous_config =brain_configuration.services.service('Pannous')
        self.assertEqual("programy.services.pannous.PannousService", pannous_config.classname)
        self.assertEqual(pannous_config.url, "http://weannie.pannous.com/api")

        self.assertIsNotNone(brain_configuration.security)
        self.assertIsNotNone(brain_configuration.security.authorisation)
        self.assertIsNotNone(brain_configuration.security.authentication)

        self.assertIsNotNone(brain_configuration.oob)
        self.assertTrue(brain_configuration.oob.exists("default"))

        self.assertIsNotNone(brain_configuration.dynamics)
        self.assertIsNotNone(brain_configuration.dynamics.dynamic_sets)

        self.assertIsNotNone(brain_configuration.dynamics.dynamic_maps)
        self.assertIsNotNone(brain_configuration.dynamics.dynamic_vars)
