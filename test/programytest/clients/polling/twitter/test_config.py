import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class TwitterConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            twitter:
              polling_interval: 59
              rate_limit_sleep: 900
              use_status: true
              use_direct_message: true
              auto_follow: true
              storage: file
              storage_location: ./storage/twitter.data
              welcome_message: Thanks for following me
        """, ConsoleConfiguration(), ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        self.assertEqual(59, twitter_config.polling_interval)
        self.assertEqual(900, twitter_config.rate_limit_sleep)
        self.assertTrue(twitter_config.use_status)
        self.assertTrue(twitter_config.use_direct_message)
        self.assertTrue(twitter_config.auto_follow)
        self.assertEquals("file", twitter_config.storage)
        self.assertEquals("./storage/twitter.data", twitter_config.storage_location)
        self.assertEquals("Thanks for following me", twitter_config.welcome_message)

    def test_to_yaml_with_defaults(self):
        config = TwitterConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEquals(data['polling_interval'], 0)
        self.assertEquals(data['rate_limit_sleep'], -1)
        self.assertEquals(data['use_status'], False)
        self.assertEquals(data['use_direct_message'], False)
        self.assertEquals(data['auto_follow'], False)
        self.assertEquals(data['storage'], 'file')
        self.assertEquals(data['storage_location'], './storage/twitter.data')
        self.assertEquals(data['welcome_message'], "Thanks for following me.")

        self.assertEquals(data['bot'], 'bot')
        self.assertEquals(data['license_keys'], "./config/license.keys")
        self.assertEquals(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEquals(data['renderer'], "programy.clients.render.text.TextRenderer")
