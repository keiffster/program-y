import unittest
import os
import json

from programy.utils.license.keys import LicenseKeys
from programy.utils.newsapi.newsapi import NewsAPI, NewsArticle

class NewsArticleTests(unittest.TestCase):

    def test_init(self):
        article = NewsArticle()
        self.assertIsNotNone(article)
        self.assertIsNone(article.title)
        self.assertIsNone(article.description)
        self.assertIsNone(article.published_at)
        self.assertIsNone(article.author)
        self.assertIsNone(article.url)
        self.assertIsNone(article.url_to_image)

    def test_parse_json(self):
        article = NewsArticle()
        data = json.loads("""
        {
            "title": "title",
            "description": "description",
            "publishedAt": "published_at",
            "author": "author",
            "url": "url",
            "urlToImage": "url_to_image"
        }
        """)
        article.parse_json(data)
        self.assertEqual("title", article.title)
        self.assertEqual("description", article.description)
        self.assertEqual("published_at", article.published_at)
        self.assertEqual("author", article.author)
        self.assertEqual("url", article.url)
        self.assertEqual("url_to_image", article.url_to_image)

        json_data = article.to_json()
        self.assertIsNotNone(json_data)
        self.assertEqual({
            "title": "title",
            "description": "description",
            "publishedAt": "published_at",
            "author": "author",
            "url": "url",
            "urlToImage": "url_to_image"
        } , json_data)


class NewsAPIExtensionTests(unittest.TestCase):

    def setUp(self):
        self.license_keys = LicenseKeys()
        self.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_init(self):
        newsapi = NewsAPI(self.license_keys)
        self.assertIsNotNone(newsapi)