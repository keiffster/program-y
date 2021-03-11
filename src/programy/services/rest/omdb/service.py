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


class OMDBTitleSearchServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return OMDBTitleSearchServiceQuery(service)

    def parse_matched(self, matched):
        self._title = ServiceQuery._get_matched_var(matched, 0, "title")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._title = None

    def execute(self):
        return self._service.title_search(self._title)

    def aiml_response(self, response):
        payload = response['response']['payload']
        title = payload['Title']
        released = payload['Released']
        director = payload['Director']
        writers = payload['Writer']
        actors = payload['Actors']
        plot = payload['Plot']

        result = "TITLE FILM {0} RELEASED {1} DIRECTOR {2} WRITER {3} ACTORS {4} PLOT {5}".format(title, released, director,
                                                                                          writers, actors, plot)
        YLogger.debug(self, result)
        return result


class OMDBServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class OMDBService(RESTService):
    """
    """
    PATTERNS = [
        [r"TITLE\sSEARCH\s(.+)", OMDBTitleSearchServiceQuery]
    ]

    BASE_URL="http://www.omdbapi.com/"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return OMDBService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('OMDB_KEY')
        if self._api_key is None:
            YLogger.error(self, "OMDB_KEY missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "omdb.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "omdb.conf"

    def _build_title_search_url(self, title):
        url = OMDBService.BASE_URL
        url += "?apikey={0}".format(self._api_key)
        if title is not None:
            url += "&t={0}".format(title)
        return url

    def title_search(self, title):
        url = self._build_title_search_url(title)
        response = self.query('title_search', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

