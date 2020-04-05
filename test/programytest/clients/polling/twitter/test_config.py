import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class TwitterConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            twitter:
              description: Program-Y Twitter Client
              polling_interval: 60
              rate_limit_sleep: 900
            
              follow_followers: True
              respond_to_mentions: True
              respond_to_directs: False
            
              mentions: |
                #askprogramy
                #programy
            
              welcome_message: "Thanks for following me."
        """, ConsoleConfiguration(), ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        self.assertEqual("Program-Y Twitter Client", twitter_config.description)

        self.assertEqual(60, twitter_config.polling_interval)
        self.assertEqual(900, twitter_config.rate_limit_sleep)

        self.assertTrue(twitter_config.follow_followers)
        self.assertTrue(twitter_config.respond_to_mentions)
        self.assertFalse(twitter_config.respond_to_directs)

        self.assertEqual(twitter_config.mentions, ['#askprogramy', '#programy'])

        self.assertEqual("Thanks for following me.", twitter_config.welcome_message)

    def test_to_yaml_with_defaults(self):
        config = TwitterConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['polling_interval'], 60)
        self.assertEqual(data['rate_limit_sleep'], 900)

        self.assertEqual(data['follow_followers'], True)
        self.assertEqual(data['respond_to_mentions'], True)
        self.assertEqual(data['respond_to_directs'], False)

        self.assertEqual(data['welcome_message'], "Thanks for following me.")

        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        self.assertTrue('bots' in data)
        self.assertTrue('bot' in data['bots'])
        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

        self.assertTrue('brains' in data['bots']['bot'])
        self.assertTrue('brain' in data['bots']['bot']['brains'])

    def test_to_yaml_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            other:
        """, ConsoleConfiguration(), ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        self.assertEqual(60, twitter_config.polling_interval)
        self.assertEqual(900, twitter_config.rate_limit_sleep)

        self.assertTrue(twitter_config.follow_followers)
        self.assertTrue(twitter_config.respond_to_mentions)
        self.assertFalse(twitter_config.respond_to_directs)

        self.assertEqual("Thanks for following me.", twitter_config.welcome_message)
