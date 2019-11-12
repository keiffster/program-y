import json
import unittest

from programy.utils.newsapi.newsapi import NewsAPI
from programytest.client import TestClient


class MockResponse(object):

    def __init__(self, status_code, headers, data):
        self.status_code = status_code
        self.headers = headers
        self.data = data

    def json(self):
        return self.data


class MockNewsApiApi(object):

    def __init__(self):
        self._repsonse = ""

    @property
    def response(self):
        return self._repsonse

    @response.setter
    def response(self, response):
        self._repsonse = response

    def get_news(self, url):
        return self._repsonse


class NewsAPITests(unittest.TestCase):

    def test_missing_license_keys(self):
        with self.assertRaises(Exception):
            _ = NewsAPI(None)

    def test_missing_keys(self):
        client = TestClient()

        with self.assertRaises(Exception):
            _ = NewsAPI(client.license_keys)

    def test_format_url(self):
        self.assertEqual("https://newsapi.org/v1/articles?source=testservice&sortBy=top&apiKey=key", NewsAPI._format_url("testservice", "key"))
        self.assertEqual("https://newsapi.org/v1/articles?source=testservice&sortBy=bottom&apiKey=key", NewsAPI._format_url("testservice", "key", sort_by="bottom"))

    def test_get_headlines(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title",
                "description":  "test description",
                "publishedAt":  "test publishedAt",
                "author":       "test author",
                "url":          "test url",
                "urlToImage":   "test urlToImage"
                }
            ]
        }
        """))

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        headlines = newsapi.get_headlines(NewsAPI.UK_NEWS)
        self.assertIsNotNone(headlines)

        headlines = newsapi.get_headlines("Other")
        self.assertIsNotNone(headlines)
        self.assertEquals([], headlines)

    def test_get_news_feed_articles(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title",
                "description":  "test description",
                "publishedAt":  "test publishedAt",
                "author":       "test author",
                "url":          "test url",
                "urlToImage":   "test urlToImage"
                }
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(1, len(articles))
        self.assertEqual("test title", articles[0].title)
        self.assertEqual("test description", articles[0].description)
        self.assertEqual("test publishedAt", articles[0].published_at)
        self.assertEqual("test author", articles[0].author)
        self.assertEqual("test url", articles[0].url)
        self.assertEqual("test urlToImage", articles[0].url_to_image)

    def test_get_news_feed_articles_max_articles_1(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title1",
                "description":  "test description1",
                "publishedAt":  "test publishedAt1",
                "author":       "test author1",
                "url":          "test url1",
                "urlToImage":   "test urlToImage1"
                },
                {
                "title":        "test title2",
                "description":  "test description2",
                "publishedAt":  "test publishedAt2",
                "author":       "test author2",
                "url":          "test url2",
                "urlToImage":   "test urlToImage2"
                }
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 1, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(1, len(articles))
        self.assertEqual("test title1", articles[0].title)
        self.assertEqual("test description1", articles[0].description)
        self.assertEqual("test publishedAt1", articles[0].published_at)
        self.assertEqual("test author1", articles[0].author)
        self.assertEqual("test url1", articles[0].url)
        self.assertEqual("test urlToImage1", articles[0].url_to_image)

    def test_get_news_feed_articles_max_articles_99(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title1",
                "description":  "test description1",
                "publishedAt":  "test publishedAt1",
                "author":       "test author1",
                "url":          "test url1",
                "urlToImage":   "test urlToImage1"
                },
                {
                "title":        "test title2",
                "description":  "test description2",
                "publishedAt":  "test publishedAt2",
                "author":       "test author2",
                "url":          "test url2",
                "urlToImage":   "test urlToImage2"
                }
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 99, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(2, len(articles))
        self.assertEqual("test title1", articles[0].title)
        self.assertEqual("test description1", articles[0].description)
        self.assertEqual("test publishedAt1", articles[0].published_at)
        self.assertEqual("test author1", articles[0].author)
        self.assertEqual("test url1", articles[0].url)
        self.assertEqual("test urlToImage1", articles[0].url_to_image)

    def test_get_news_feed_articles_none_200_response(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(401, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title",
                "description":  "test description",
                "publishedAt":  "test publishedAt",
                "author":       "test author",
                "url":          "test url",
                "urlToImage":   "test urlToImage"
                }
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))

    def test_get_news_feed_articles_content_not_json(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/xml"}, None)

        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))

    def test_get_news_feed_articles_no_articles(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))

    def test_get_news_feed_articles_no_articles_included(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))

    def test_abc_news_au(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title",
                "description":  "test description",
                "publishedAt":  "test publishedAt",
                "author":       "test author",
                "url":          "test url",
                "urlToImage":   "test urlToImage"
                }
            ]
        }
        """))

        response = NewsAPI.abc_news_au("testservice", 10, False, False)
        self.assertIsNotNone(response)
