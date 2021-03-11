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
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class GNewsTopics:

    TOPICS = [
        "world",
        "nation",
        "business",
        "technology",
        "entertainment",
        "sports",
        "science",
        "health",
    ]


class GNewsSearchQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GNewsSearchQuery(service)

    def parse_matched(self, matched):
        self._query = ServiceQuery._get_matched_var(matched, 0, "query")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._query = None

    def execute(self):
        return self._service.search(self._query)

    def aiml_response(self, response):
        result = "SEARCH <ul>" + "".join("<li>"+x['title']+"</li>" for x in response['response']['payload']['articles']) + "</ul>"
        YLogger.debug(self, result)
        return result


class GNewsTopNewsQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GNewsTopNewsQuery(service)

    def parse_matched(self, matched):
        self._lang = ServiceQuery._get_matched_var(matched, 0, "lang", optional=True)
        self._country = ServiceQuery._get_matched_var(matched, 1, "country", optional=True)

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._lang = None
        self._country = None

    def execute(self):
        return self._service.top_news(lang=self._lang, country=self._country)

    def aiml_response(self, response):
        result = "TOPNEWS <ul>" + "".join("<li>"+x['title']+"</li>" for x in response['response']['payload']['articles']) + "</ul>"
        YLogger.debug(self, result)
        return result


class GNewsTopicsListQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GNewsTopicsListQuery(service)

    def parse_matched(self, matched):
        pass

    def __init__(self, service):
        ServiceQuery.__init__(self, service)

    def execute(self):
        return {'response': {'status': 'success', 'payload': {'topics': GNewsTopics.TOPICS}}}

    def aiml_response(self, response):
        result = "TOPICS <ul>" + "".join("<li>"+x+"</li>" for x in response['response']['payload']['topics']) + "</ul>"
        YLogger.debug(self, result)
        return result


class GNewsTopicQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GNewsTopicQuery(service)

    def parse_matched(self, matched):
        self._topic = ServiceQuery._get_matched_var(matched, 0, "topic")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._topic = None

    def execute(self):
        return self._service.topics(self._topic)

    def aiml_response(self, response):
        payload = response['response']['payload']
        articles = payload['articles']
        result = "<ul>"
        result += "\n".join(["<li>{0}</li>".format(article['title']) for article in articles])
        result += "</ul>"
        result = "TOPIC {0}".format(result)
        YLogger.debug(self, result)
        return result


class GNewsServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class GNewsService(RESTService):
    """
    https://gnews.io/docs/v3#introduction
    """
    PATTERNS = [
        [r"SEARCH\s(.+)", GNewsSearchQuery],
        [r"TOPNEWS\s(.+)\s(.+)", GNewsTopNewsQuery],
        [r"TOPNEWS", GNewsTopNewsQuery],
        [r"TOPICS", GNewsTopicsListQuery],
        [r"TOPIC\s(\w+)", GNewsTopicQuery]
    ]

    SEARCH_BASE_URL=" https://gnews.io/api/v3/search"
    TOPNEWS_BASE_URL=" https://gnews.io/api/v3/top-news"
    TOPICS_BASE_URL="https://gnews.io/api/v3/topics"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._token = None

    def patterns(self) -> list:
        return GNewsService.PATTERNS

    def initialise(self, client):
        self._token = client.license_keys.get_key("GNEWS_TOKEN")
        if self._token is None:
            YLogger.error(self, "GNEWS_TOKEN missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "gnews.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "gnews.conf"

    def _build_search_url(self, query, lang=None, country=None, max=None, image=None, mindate=None, maxdate=None, specific=None):
        url = GNewsService.SEARCH_BASE_URL
        url += "?token={0}".format(self._token)

        if query is not None:
            url += "&q={0}".format(urllib.parse.quote_plus(query))

        if lang is not None:
            url += "&lang={0}".format(lang)

        if country is not None:
            url += "&country={0}".format(country)

        if max is not None:
            url += "&max={0}".format(max)

        if image is not None:
            url += "&image={0}".format(image)

        if mindate is not None:
            url += "&mindate={0}".format(mindate)

        if maxdate is not None:
            url += "&maxdate={0}".format(maxdate)

        if specific is not None:
            url += "&in={0}".format(specific)

        return url

    def _build_top_news_url(self, lang=None, country=None, max=None, image=None):
        url = GNewsService.TOPNEWS_BASE_URL
        url += "?token={0}".format(self._token)

        if lang is not None:
            url += "&lang={0}".format(lang)

        if country is not None:
            url += "&country={0}".format(country)

        if max is not None:
            url += "&max={0}".format(max)

        if image is not None:
            url += "&image={0}".format(image)

        return url

    def _build_topics_url(self, topic, lang=None, country=None, max=None, image=None):
        url = GNewsService.TOPICS_BASE_URL

        url += "/{0}".format(topic)

        url += "?token={0}".format(self._token)

        if lang is not None:
            url += "&lang={0}".format(lang)

        if country is not None:
            url += "&country={0}".format(country)

        if max is not None:
            url += "&max={0}".format(max)

        if image is not None:
            url += "&image={0}".format(image)

        return url

    def search(self, query, lang=None, country=None, max=None, image=None, mindate=None, maxdate=None, specific=None):
        url = self._build_search_url(query, lang, country, max, image, mindate, maxdate, specific)
        response = self.query('search', url)
        return response

    def top_news(self, lang=None, country=None, max=None, image=None):
        if lang is not None:
            lang = lang.lower()
        if country is not None:
            country = country.lower()
        url = self._build_top_news_url(lang, country, max, image)
        response = self.query('top_news', url)
        return response

    def _validate_topic(self, topic):
        if topic not in GNewsTopics.TOPICS:
            raise GNewsServiceException("Invalid topic [%s]" % topic)

    def topics(self, topic, lang=None, country=None, max=None, image=None):
        topic = topic.lower()
        self._validate_topic(topic)
        url = self._build_topics_url(topic, lang, country, max, image)
        response = self.query('topics', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

