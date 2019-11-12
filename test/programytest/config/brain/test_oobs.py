import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.oobs import BrainOOBSConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BrainOOBsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oob:
              default:
                classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
              dial:
                classname: programy.oob.defaults.dial.DialOutOfBandProcessor
              email:
                classname: programy.oob.defaults.email.EmailOutOfBandProcessor
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(oobs_config.exists("default"))
        self.assertTrue(oobs_config.exists("dial"))
        self.assertTrue(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))

        self.assertIsNotNone(oobs_config.oob("dial"))
        self.assertIsNone(oobs_config.oob("dialX"))

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            oobs:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(oobs_config.exists("default"))
        self.assertFalse(oobs_config.exists("dial"))
        self.assertFalse(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(oobs_config.exists("default"))
        self.assertFalse(oobs_config.exists("dial"))
        self.assertFalse(oobs_config.exists("email"))
        self.assertFalse(oobs_config.exists("Other"))

    def test_to_yaml_with_defaults(self):
        oobs_config = BrainOOBSConfiguration()
        data = {}
        oobs_config.to_yaml(data, defaults=True)

        self.assertEquals({'default': {'classname': 'programy.oob.defaults.default.DefaultOutOfBandProcessor'},
                           'alarm': {'classname': 'programy.oob.defaults.alarm.AlarmOutOfBandProcessor'},
                           'camera': {'classname': 'programy.oob.defaults.camera.CameraOutOfBandProcessor'},
                           'clear': {'classname': 'programy.oob.defaults.clear.ClearOutOfBandProcessor'},
                           'dial': {'classname': 'programy.oob.defaults.dial.DialOutOfBandProcessor'},
                           'dialog': {'classname': 'programy.oob.defaults.dialog.DialogOutOfBandProcessor'},
                           'email': {'classname': 'programy.oob.defaults.email.EmailOutOfBandProcessor'},
                           'geomap': {'classname': 'programy.oob.defaults.map.MapOutOfBandProcessor'},
                           'schedule': {'classname': 'programy.oob.defaults.schedule.ScheduleOutOfBandProcessor'},
                           'search': {'classname': 'programy.oob.defaults.search.SearchOutOfBandProcessor'},
                           'sms': {'classname': 'programy.oob.defaults.sms.SMSOutOfBandProcessor'},
                           'url': {'classname': 'programy.oob.defaults.url.URLOutOfBandProcessor'},
                           'wifi': {'classname': 'programy.oob.defaults.wifi.WifiOutOfBandProcessor'}}, data)

    def test_to_yaml_without_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
         brain:
             oob:
               default:
                 classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
               dial:
                 classname: programy.oob.defaults.dial.DialOutOfBandProcessor
               email:
                 classname: programy.oob.defaults.email.EmailOutOfBandProcessor
         """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        oobs_config = BrainOOBSConfiguration()
        oobs_config.load_config_section(yaml, brain_config, ".")

        data = {}
        oobs_config.to_yaml(data, defaults=False)

        self.assertEquals({'default': {'classname': 'programy.oob.defaults.default.DefaultOutOfBandProcessor'},
                           'dial': {'classname': 'programy.oob.defaults.dial.DialOutOfBandProcessor'},
                           'email': {'classname': 'programy.oob.defaults.email.EmailOutOfBandProcessor'}}, data)
