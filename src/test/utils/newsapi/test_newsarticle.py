import unittest
import json

from programy.utils.newsapi.newsapi import NewsArticle

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

    def test_missing_values(self):
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

        self.assertIsNone(article._get_json_attribute(data, "other_value"))
        self.assertEqual("Default", article._get_json_attribute(data, "other_value", "Default"))

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

