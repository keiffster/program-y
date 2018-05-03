import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.polling.xmpp.config import XmppConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

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

        self.assertEquals('talk.google.com', xmpp_config.server)
        self.assertEquals(5222, xmpp_config.port)
        self.assertTrue(xmpp_config.xep_0030)
        self.assertTrue(xmpp_config.xep_0004)
        self.assertTrue(xmpp_config.xep_0060)
        self.assertTrue(xmpp_config.xep_0199)

    def test_to_yaml_with_defaults(self):
        config = XmppConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEquals(data['server'], "talk.google.com")
        self.assertEquals(data['port'], 5222)
        self.assertEquals(data['xep_0030'], True)
        self.assertEquals(data['xep_0004'], True)
        self.assertEquals(data['xep_0060'], True)
        self.assertEquals(data['xep_0199'], True)

        self.assertEquals(data['bot'], 'bot')
        self.assertEquals(data['license_keys'], "./config/license.keys")
        self.assertEquals(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEquals(data['renderer'], "programy.clients.render.text.TextRenderer")
