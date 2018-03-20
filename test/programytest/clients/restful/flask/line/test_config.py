import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.restful.flask.line.config import LineConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class LineConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        line:
          host: 127.0.0.1
          port: 5000
          debug: false
          unknown_command: Sorry, that is not a command I have been taught yet!
          unknown_command_srai: YLINE_UNKNOWN_COMMAND
        """, ConsoleConfiguration(), ".")

        line_config = LineConfiguration()
        line_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", line_config.host)
        self.assertEqual(5000, line_config.port)
        self.assertEqual(False, line_config.debug)
        self.assertEquals(line_config.unknown_command, "Sorry, that is not a command I have been taught yet!")
        self.assertEquals(line_config.unknown_command_srai, "YLINE_UNKNOWN_COMMAND")

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        line:
        """, ConsoleConfiguration(), ".")

        line_config = LineConfiguration()
        line_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", line_config.host)
        self.assertEqual(80, line_config.port)
        self.assertEqual(False, line_config.debug)
