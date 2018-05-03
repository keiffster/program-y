import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.bot.bot import BotConfiguration

class ConsoleConfigurationTests(unittest.TestCase):
    
    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          bot: bot
          default_userid: console
          prompt: $
        """, ConsoleConfiguration(), ".")

        config = ConsoleConfiguration()
        config.load_configuration(yaml, ".")

        self.assertEquals("console", config.default_userid)
        self.assertEquals("$", config.prompt)

        self.assertIsNotNone(config.configurations)
        self.assertEquals(1, len(config.configurations))
        self.assertIsInstance(config.configurations[0], BotConfiguration)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        config = ConsoleConfiguration()
        config.load_configuration(yaml, ".")

        self.assertIsNotNone(config.configurations)
        self.assertEquals(1, len(config.configurations))

    def test_to_yaml_with_defaults(self):
        config = ConsoleConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEquals('console', data['default_userid'])
        self.assertEquals('>>>', data['prompt'])

        self.assertEquals(data['bot'], 'bot')
        self.assertEquals(data['license_keys'], "./config/license.keys")
        self.assertEquals(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEquals(data['renderer'], "programy.clients.render.text.TextRenderer")

    def test_to_yaml_without_defaults(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          bot: bot
          default_userid: console
          prompt: $
          license_keys: ./config/license.keys
          bot_selector: programy.clients.client.DefaultBotSelector
          renderer: programy.clients.render.text.TextRenderer
        """, ConsoleConfiguration(), ".")

        config = ConsoleConfiguration()
        config.load_configuration(yaml, ".")

        data = {}
        config.to_yaml(data, False)

        self.assertEquals('console', data['default_userid'])
        self.assertEquals('$', data['prompt'])

        self.assertEquals(data['bot'], 'bot')
        self.assertEquals(data['license_keys'], "./config/license.keys")
        self.assertEquals(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEquals(data['renderer'], "programy.clients.render.text.TextRenderer")
