import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.xmpp import XmppConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

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
        xmpp_config.load_config_section(yaml, ".")

        self.assertEquals('talk.google.com', xmpp_config.server)
        self.assertEquals(5222, xmpp_config.port)
        self.assertTrue(xmpp_config.xep_0030)
        self.assertTrue(xmpp_config.xep_0004)
        self.assertTrue(xmpp_config.xep_0060)
        self.assertTrue(xmpp_config.xep_0199)

