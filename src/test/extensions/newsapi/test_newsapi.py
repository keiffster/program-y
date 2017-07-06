import unittest

from programy.extensions.newsapi.newsapi import NewsAPIExtension

class MockNewsAPI(object):

    def __init__(self, license_keys):
        pass

class MockNewsAPIExtension(NewsAPIExtension):

    def get_news_api_api(self, bot, clientid):
        return  MockNewsAPI(bot.license_keys)



class NewsAPIExtensionTests(unittest.TestCase):

    def test_parse_data(self):

        extension = NewsAPIExtension()
        self.assertIsNotNone(extension)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC")
        self.assertEqual("BBC", source)
        self.assertEqual(10, max)
        self.assertEqual(False, sort)
        self.assertEqual(False, reverse)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC MAX 20")
        self.assertEqual("BBC", source)
        self.assertEqual(20, max)
        self.assertEqual(False, sort)
        self.assertEqual(False, reverse)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC MAX 20 SORT TRUE")
        self.assertEqual("BBC", source)
        self.assertEqual(20, max)
        self.assertEqual(True, sort)
        self.assertEqual(False, reverse)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC MAX 20 SORT FALSE")
        self.assertEqual("BBC", source)
        self.assertEqual(20, max)
        self.assertEqual(False, sort)
        self.assertEqual(False, reverse)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC MAX 20 SORT ERROR")
        self.assertEqual("BBC", source)
        self.assertEqual(20, max)
        self.assertEqual(False, sort)
        self.assertEqual(False, reverse)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC MAX 20 SORT TRUE REVERSE TRUE")
        self.assertEqual("BBC", source)
        self.assertEqual(20, max)
        self.assertEqual(True, sort)
        self.assertEqual(True, reverse)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC MAX 20 SORT TRUE REVERSE FALSE")
        self.assertEqual("BBC", source)
        self.assertEqual(20, max)
        self.assertEqual(True, sort)
        self.assertEqual(False, reverse)

        source, max, sort, reverse = extension.parse_data("SOURCE BBC MAX 20 SORT TRUE REVERSE ERROR")
        self.assertEqual("BBC", source)
        self.assertEqual(20, max)
        self.assertEqual(True, sort)
        self.assertEqual(False, reverse)
