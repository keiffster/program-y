import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.line_client import LineConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class LineConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        line:
          host: 127.0.0.1
          port: 5000
          debug: false
        """, ConsoleConfiguration(), ".")

        line_config = LineConfiguration()
        line_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", line_config.host)
        self.assertEqual(5000, line_config.port)
        self.assertEqual(False, line_config.debug)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        line:
        """, ConsoleConfiguration(), ".")

        line_config = LineConfiguration()
        line_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", line_config.host)
        self.assertEqual(5000, line_config.port)
        self.assertEqual(False, line_config.debug)
