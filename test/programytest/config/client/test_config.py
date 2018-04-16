import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.config import ClientConfigurationData
from programy.clients.events.console.config import ConsoleConfiguration

class ClientConfigurationDataTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          bot:  bot
          prompt: ">>>"
          license_keys: $BOT_ROOT/config/license.keys
          bot_selector: programy.clients.client.DefaultBotSelector
          renderer: programy.clients.render.text.TextRenderer
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        client_config = ClientConfigurationData("test")
        client_config.load_configuration(yaml, bot_config, ".")

        self.assertEquals("./config/license.keys", client_config.license_keys)

        self.assertEquals("programy.clients.client.DefaultBotSelector", client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEquals("Scheduler1", client_config.scheduler.name)
        self.assertEquals(0, client_config.scheduler.debug_level)
        self.assertTrue(client_config.scheduler.add_listeners)
        self.assertTrue(client_config.scheduler.remove_all_jobs)

        self.assertEquals("programy.clients.render.text.TextRenderer", client_config.renderer)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        client_config = ClientConfigurationData("test")
        client_config.load_configuration(yaml, bot_config, ".")

        self.assertIsNone(client_config.license_keys)

        self.assertIsNone(client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEquals(None, client_config.scheduler.name)
        self.assertEquals(0, client_config.scheduler.debug_level)
        self.assertFalse(client_config.scheduler.add_listeners)
        self.assertFalse(client_config.scheduler.remove_all_jobs)

        self.assertIsNone(client_config.renderer)
