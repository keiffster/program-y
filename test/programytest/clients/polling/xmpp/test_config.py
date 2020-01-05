import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.polling.xmpp.config import XmppConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class XmppConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            xmpp:
                server: talk.google.com
                port: 5222
                xep_0030: true
                xep_0004: true
                xep_0060: true
                xep_0199: true
        """, ConsoleConfiguration(), ".")

        xmpp_config = XmppConfiguration()
        xmpp_config.load_configuration(yaml, ".")

        self.assertEqual('talk.google.com', xmpp_config.server)
        self.assertEqual(5222, xmpp_config.port)
        self.assertTrue(xmpp_config.xep_0030)
        self.assertTrue(xmpp_config.xep_0004)
        self.assertTrue(xmpp_config.xep_0060)
        self.assertTrue(xmpp_config.xep_0199)

    def test_to_yaml_with_defaults(self):
        config = XmppConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['server'], "talk.google.com")
        self.assertEqual(data['port'], 5222)
        self.assertEqual(data['xep_0030'], True)
        self.assertEqual(data['xep_0004'], True)
        self.assertEqual(data['xep_0060'], True)
        self.assertEqual(data['xep_0199'], True)

        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        self.assertTrue('bots' in data)
        self.assertTrue('bot' in data['bots'])
        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

        self.assertTrue('brains' in data['bots']['bot'])
        self.assertTrue('brain' in data['bots']['bot']['brains'])
