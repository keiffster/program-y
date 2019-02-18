import unittest

from programy.clients.events.tcpsocket.config import SocketConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration


class SocketConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        socket:
          host: 127.0.0.1
          port: 9999
          queue: 5
          max_buffer: 1024
          debug: true
          """, ConsoleConfiguration(), ".")

        socket_config = SocketConfiguration()
        socket_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", socket_config.host)
        self.assertEqual(9999, socket_config.port)
        self.assertEqual(5, socket_config.queue)
        self.assertEqual(1024, socket_config.max_buffer)
        self.assertEqual(True, socket_config.debug)

    def test_to_yaml_with_defaults(self):
        config = SocketConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual("0.0.0.0", data['host'])
        self.assertEqual(80, data['port'])
        self.assertEqual(5, data['queue'])
        self.assertEqual(1024, data['max_buffer'])
        self.assertEqual(False, data['debug'])

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

    def test_to_yaml_without_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        socket:
          host: 127.0.0.1
          port: 9999
          queue: 5
          max_buffer: 1024
          debug: true
          bot: bot
          default_userid: console
          prompt: $
          bot_selector: programy.clients.client.DefaultBotSelector
          renderer: programy.clients.render.text.TextRenderer
        """, ConsoleConfiguration(), ".")

        config = SocketConfiguration()
        config.load_configuration(yaml, ".")

        data = {}
        config.to_yaml(data, False)

        self.assertEqual("127.0.0.1", data['host'])
        self.assertEqual(9999, data['port'])
        self.assertEqual(5, data['queue'])
        self.assertEqual(1024, data['max_buffer'])
        self.assertEqual(True, data['debug'])

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")
