import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.restful.flask.webchat.config import WebChatConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class WebChatConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        webchat:
          host: 127.0.0.1
          port: 5000
          debug: false
          use_api_keys: false
          cookie_id: ProgramYSession
          cookie_expires: 90
        """, ConsoleConfiguration(), ".")

        webchat_config = WebChatConfiguration()
        webchat_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", webchat_config.host)
        self.assertEqual(5000, webchat_config.port)
        self.assertEqual(False, webchat_config.debug)
        self.assertEqual(False, webchat_config.use_api_keys)
        self.assertEqual("ProgramYSession", webchat_config.cookie_id)
        self.assertEqual(90, webchat_config.cookie_expires)

    def test_to_yaml_with_defaults(self):
        config = WebChatConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['cookie_id'], "ProgramYSession")
        self.assertEqual(90, data['cookie_expires'])

    def test_to_yaml_with_no_defaults(self):
        config = WebChatConfiguration()

        data = {}
        config.to_yaml(data, False)

        self.assertEqual(data['cookie_id'], "ProgramYSession")
        self.assertEqual(90, data['cookie_expires'])
