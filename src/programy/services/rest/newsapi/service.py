"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import urllib.parse
import os
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException
from programy.utils.logging.ylogger import YLogger


class NewsAPIFeedEverythingServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return NewsAPIFeedEverythingServiceQuery(service)

    def parse_matched(self, matched):
        self._query = ServiceQuery._get_matched_var(matched, 0, "query")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._query = None

    def execute(self):
        return self._service.get_everything(self._query)

    def aiml_response(self, response):
        payload = response['response']['payload']
        articles = payload['articles']
        headlines = ["<li>{0}</li>\n".format(x['title']) for x in articles]
        result = "EVERYTHING <ul>{0}</ul>".format("".join(headlines))
        YLogger.debug(self, result)
        return result


class NewsAPIFeedCollectionsServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return NewsAPIFeedCollectionsServiceQuery(service)

    def __init__(self, service):
        ServiceQuery.__init__(self, service)

    def execute(self):
        return self._service.get_collections()

    def aiml_response(self, response):
        result = "COLLECTIONS {0}".format(response)
        YLogger.debug(self, result)
        return result


class NewsAPIServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class NewsAPIService(RESTService):
    """
    """
    PATTERNS = [
        [r"COLLECTIONS", NewsAPIFeedCollectionsServiceQuery],
        [r"EVERYTHING\s(.+)", NewsAPIFeedEverythingServiceQuery]
    ]

    COLLECTIONS = {
        "BUSINESS": "business",
        "ENTERTAINMENT": " entertainment",
        "GAMING": "gaming",
        "MUSIC": "music",
        "SCIENCE AND NATURE": "science_and_nature",
        "SPORT": "sport",
        "TECHNOLOGY": "technology",
        "UK NEWS": "uk_news",
        "UK NEWSPAPERS": "uk_newspapers"
    }

    NEWSAPI_SOURCES_URL = "https://newsapi.org/v2/sources?apiKey={0}"
    NEWSAPI_EVERYTHING_URL = "https://newsapi.org/v2/everything?q={0}&sortBy={1}&apiKey={2}"
    NEWSAPI_HEADLINE_URL = "https://newsapi.org/v2/top-headlines?country={0}&category={1}&apiKey={2}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return NewsAPIService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('NEWSAPI_API_KEY')
        if self._api_key is None:
            YLogger.error(self, "NEWSAPI_API_KEY missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "newsapi.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "newsapi.conf"

    def get_collections(self):
        return {
            'response': {
                'service': self.name,
                'category': self.category,
                'status': 'success',
                'call': 'DIRECT',
                'payload': {
                    'collections': NewsAPIService.COLLECTIONS.keys()[:]
                }
            }
        }

    def _build_sources_url(self):
        url = NewsAPIService.NEWSAPI_SOURCES_URL.format(self._api_key)
        return url

    def get_sources(self):
        url = self._build_sources_url()
        response = self.query('get_sources', url)
        return response

    def _build_everything_url(self, query, sortBy):
        url = NewsAPIService.NEWSAPI_EVERYTHING_URL.format(query, sortBy, self._api_key)
        return url

    def get_everything(self, query, sortBy="top"):
        url = self._build_everything_url(query, sortBy)
        response = self.query('get_everything', url)
        return response

    def _build_headlines_url(self, country, sortBy):
        url = NewsAPIService.NEWSAPI_HEADLINE_URL.format(country, sortBy, self._api_key)
        return url

    def get_headlines(self, country, sortBy="top"):
        url = self._build_headlines_url(country, sortBy)
        response = self.query('get_headlines', url)
        return response

    def get_business(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.bloomberg(api_key, max_articles, sort, reverse))
        articles.extend(self.business_insider(api_key, max_articles, sort, reverse))
        articles.extend(self.business_insider_uk(api_key, max_articles, sort, reverse))
        articles.extend(self.cnbc(api_key, max_articles, sort, reverse))
        articles.extend(self.financial_times(api_key, max_articles, sort, reverse))
        articles.extend(self.fortune(api_key, max_articles, sort, reverse))
        articles.extend(self.the_economist(api_key, max_articles, sort, reverse))
        articles.extend(self.the_wall_street_journal(api_key, max_articles, sort, reverse))
        return articles

    def get_entertainment(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.buzzfeed(api_key, max_articles, sort, reverse))
        articles.extend(self.daily_mail(api_key, max_articles, sort, reverse))
        articles.extend(self.entertainment_weekly(api_key, max_articles, sort, reverse))
        articles.extend(self.mashable(api_key, max_articles, sort, reverse))
        return articles

    def get_gaming(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.ign(api_key, max_articles, sort, reverse))
        articles.extend(self.polygon(api_key, max_articles, sort, reverse))
        return articles

    def get_music(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.mtv_news(api_key, max_articles, sort, reverse))
        articles.extend(self.mtv_news_uk(api_key, max_articles, sort, reverse))
        return articles

    def get_science_and_nature(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.national_geographic(api_key, max_articles, sort, reverse))
        articles.extend(self.new_scientist(api_key, max_articles, sort, reverse))
        return articles

    def get_sport(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.bbc_sport(api_key, max_articles, sort, reverse))
        articles.extend(self.espn(api_key, max_articles, sort, reverse))
        articles.extend(self.espn_cric_info(api_key, max_articles, sort, reverse))
        articles.extend(self.football_italia(api_key, max_articles, sort, reverse))
        articles.extend(self.four_four_two(api_key, max_articles, sort, reverse))
        articles.extend(self.fox_sports(api_key, max_articles, sort, reverse))
        articles.extend(self.talksport(api_key, max_articles, sort, reverse))
        articles.extend(self.the_sport_bible(api_key, max_articles, sort, reverse))
        return articles

    def get_technology(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.ars_technica(api_key, max_articles, sort, reverse))
        articles.extend(self.engadget(api_key, max_articles, sort, reverse))
        articles.extend(self.hacker_news(api_key, max_articles, sort, reverse))
        articles.extend(self.recode(api_key, max_articles, sort, reverse))
        articles.extend(self.techcrunch(api_key, max_articles, sort, reverse))
        articles.extend(self.techradar(api_key, max_articles, sort, reverse))
        articles.extend(self.the_verge(api_key, max_articles, sort, reverse))
        return articles

    def get_uk_news(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.bbc_news(api_key, max_articles, sort, reverse))
        articles.extend(self.uk_newspapers(api_key, max_articles, sort, reverse))
        return articles

    def get_uk_newspapers(self, api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(self.the_guardian_uk(api_key, max_articles, sort, reverse))
        articles.extend(self.mirror(api_key, max_articles, sort, reverse))
        articles.extend(self.the_telegraph(api_key, max_articles, sort, reverse))
        articles.extend(self.daily_mail(api_key, max_articles, sort, reverse))
        articles.extend(self.financial_times(api_key, max_articles, sort, reverse))
        articles.extend(self.independent(api_key, max_articles, sort, reverse))
        articles.extend(self.metro(api_key, max_articles, sort, reverse))
        return articles

    def _response_to_json(self, api, response):
        return response.json()

