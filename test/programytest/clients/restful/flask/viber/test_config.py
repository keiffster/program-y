import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.restful.flask.viber.config import ViberConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class ViberConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        viber:
          host: 127.0.0.1
          port: 5000
          debug: false
          name: test
          avatar: avatar.jpg
          webhook: http://localhost
        """, ConsoleConfiguration(), ".")

        viber_config = ViberConfiguration()
        viber_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", viber_config.host)
        self.assertEqual(5000, viber_config.port)
        self.assertEqual(False, viber_config.debug)
        self.assertEqual("test", viber_config.name)
        self.assertEqual("avatar.jpg", viber_config.avatar)
        self.assertEqual("http://localhost", viber_config.webhook)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        viber:
        """, ConsoleConfiguration(), ".")

        viber_config = ViberConfiguration()
        viber_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", viber_config.host)
        self.assertEqual(80, viber_config.port)
        self.assertEqual(False, viber_config.debug)
        self.assertIsNone(viber_config.name)
        self.assertIsNone(viber_config.avatar)
        self.assertIsNone(viber_config.webhook)

    def test_to_yaml_with_defaults(self):
        config = ViberConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['name'], "Program-Y")
        self.assertEqual(data['avatar'], 'http://127.0.0.1/programy.png')
        self.assertEqual(data['webhook'], 'https://127.0.0.1/api/viber/v1.0/ask')

        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        self.assertTrue('bots' in data)
        self.assertTrue('bot' in data['bots'])
        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

        self.assertTrue('brains' in data['bots']['bot'])
        self.assertTrue('brain' in data['bots']['bot']['brains'])
