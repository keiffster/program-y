import unittest

from programy.config.sections.client.webchat import WebChatConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.console import ConsoleConfiguration

class WebChatConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        webchat:
          host: 127.0.0.1
          port: 5000
          debug: false
        """, ConsoleConfiguration(), ".")

        webchat_config = WebChatConfiguration()
        webchat_config.load_config_section(yaml, ".")

        self.assertEqual("127.0.0.1", webchat_config.host)
        self.assertEqual(5000, webchat_config.port)
        self.assertEqual(False, webchat_config.debug)

