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


class NewsAPISourcesTests(unittest.TestCase):

    def setUp(self):
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

    def test_abc_news_au(self):
        response = NewsAPI.abc_news_au("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_al_jazeera_english(self):
        response = NewsAPI.al_jazeera_english("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_ars_technica(self):
        response = NewsAPI.ars_technica("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_associated_press(self):
        response = NewsAPI.associated_press("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_bbc_news(self):
        response = NewsAPI.bbc_news("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_bbc_sport(self):
        response = NewsAPI.bbc_sport("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_bloomberg(self):
        response = NewsAPI.bloomberg("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_business_insider(self):
        response = NewsAPI.business_insider("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_business_insider_uk(self):
        response = NewsAPI.business_insider_uk("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_buzzfeed(self):
        response = NewsAPI.buzzfeed("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_cnbc(self):
        response = NewsAPI.cnbc("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_cnn(self):
        response = NewsAPI.cnn("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_daily_mail(self):
        response = NewsAPI.daily_mail("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_engadget(self):
        response = NewsAPI.engadget("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_entertainment_weekly(self):
        response = NewsAPI.entertainment_weekly("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_espn(self):
        response = NewsAPI.espn("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_espn_cric_info(self):
        response = NewsAPI.espn_cric_info("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_financial_times(self):
        response = NewsAPI.financial_times("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_football_italia(self):
        response = NewsAPI.football_italia("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_fortune(self):
        response = NewsAPI.fortune("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_four_four_two(self):
        response = NewsAPI.four_four_two("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_fox_sports(self):
        response = NewsAPI.fox_sports("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_google_news(self):
        response = NewsAPI.google_news("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_hacker_news(self):
        response = NewsAPI.hacker_news("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_ign(self):
        response = NewsAPI.ign("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_independent(self):
        response = NewsAPI.independent("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_mashable(self):
        response = NewsAPI.mashable("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_metro(self):
        response = NewsAPI.metro("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_mirror(self):
        response = NewsAPI.mirror("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_mtv_news(self):
        response = NewsAPI.mtv_news("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_mtv_news_uk(self):
        response = NewsAPI.mtv_news_uk("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_national_geographic(self):
        response = NewsAPI.national_geographic("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_new_scientist(self):
        response = NewsAPI.new_scientist("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_newsweek(self):
        response = NewsAPI.newsweek("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_new_york_magazine(self):
        response = NewsAPI.new_york_magazine("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_nfl_news(self):
        response = NewsAPI.nfl_news("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_polygon(self):
        response = NewsAPI.polygon("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_recode(self):
        response = NewsAPI.recode("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_reddit(self):
        response = NewsAPI.reddit("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_reuters(self):
        response = NewsAPI.reuters("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_talksport(self):
        response = NewsAPI.talksport("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_techcrunch(self):
        response = NewsAPI.techcrunch("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_techradar(self):
        response = NewsAPI.techradar("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_economist(self):
        response = NewsAPI.the_economist("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_guardian_au(self):
        response = NewsAPI.the_guardian_au("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_guardian_uk(self):
        response = NewsAPI.the_guardian_uk("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_huffington_post(self):
        response = NewsAPI.the_huffington_post("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_new_york_times(self):
        response = NewsAPI.the_new_york_times("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_next_web(self):
        response = NewsAPI.the_next_web("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_sport_bible(self):
        response = NewsAPI.the_sport_bible("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_telegraph(self):
        response = NewsAPI.the_telegraph("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_verge(self):
        response = NewsAPI.the_verge("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_wall_street_journal(self):
        response = NewsAPI.the_wall_street_journal("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_the_washington_post(self):
        response = NewsAPI.the_washington_post("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_time(self):
        response = NewsAPI.time("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_usa_today(self):
        response = NewsAPI.usa_today("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_business(self):
        response = NewsAPI.business("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_entertainment(self):
        response = NewsAPI.entertainment("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_gaming(self):
        response = NewsAPI.gaming("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_music(self):
        response = NewsAPI.music("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_science_and_nature(self):
        response = NewsAPI.science_and_nature("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_sport(self):
        response = NewsAPI.sport("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_technology(self):
        response = NewsAPI.technology("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_uk_news(self):
        response = NewsAPI.uk_news("testservice", 10, False, False)
        self.assertIsNotNone(response)

    def test_uk_newspapers(self):
        response = NewsAPI.uk_newspapers("testservice", 10, False, False)
        self.assertIsNotNone(response)
