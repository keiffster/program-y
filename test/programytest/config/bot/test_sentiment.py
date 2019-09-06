import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.bot.sentiment import BotSentimentAnalyserConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BotSentimentAnalyserConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            sentiment:
                classname: programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser
                scores: programy.nlp.sentiment.scores.SentimentScores
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser", sentiment_config.classname)
        self.assertEqual("programy.nlp.sentiment.scores.SentimentScores", sentiment_config.scores)

    def test_with_default_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            sentiment:
                classname: programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser", sentiment_config.classname)
        self.assertEqual("programy.nlp.sentiment.scores.SentimentScores", sentiment_config.scores)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            sentiment:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(sentiment_config.classname)
        self.assertIsNone(sentiment_config.scores)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        sentiment_config = BotSentimentAnalyserConfiguration()
        sentiment_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(sentiment_config.classname)
        self.assertIsNone(sentiment_config.scores)

