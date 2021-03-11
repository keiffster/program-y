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


class YelpEventsSearchQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return YelpEventsSearchQuery(service)

    def parse_matched(self, matched):
        self._location = ServiceQuery._get_matched_var(matched, 0, "location")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._location = None

    def execute(self):
        return self._service.search(self._location)

    def aiml_response(self, response):
        payload = response['response']['payload']
        events = payload["events"]
        result = "<ul>\n"
        for event in events:
            result += "<li>{0} - {1}</li>\n".format(event['name'], event['description'])
        result += "<ul>"
        return result


class YelpEventsSearchServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class YelpEventsSearchService(RESTService):
    """
    https://www.yelp.co.uk/developers/documentation/v3/event_search
    """
    PATTERNS = [
        [r"EVENTS\sSEARCH\sLOCATION\s(.+)", YelpEventsSearchQuery]
    ]

    EVENTS_SEARCH_URL="https://api.yelp.com/v3/events"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None
        
    def initialise(self, client):
        self._api_key = client.license_keys.get_key('YELP_API_KEY')
        if self._api_key is None:
            YLogger.error(self, "YELP_API_KEY missing from license.keys, service will not function correctly!")

    def patterns(self) -> list:
        return YelpEventsSearchService.PATTERNS

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "events.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "events.conf"

    def _build_search_url(self, location, locale):
        url = YelpEventsSearchService.EVENTS_SEARCH_URL
        url += "?location={0}&locale={1}".format(location, locale)
        return url

    def _build_search_headers(self):
        return {"Authorization": "Bearer {0}".format(self._api_key)}

    def search(self, location, locale="en_GB"):
        url = self._build_search_url(location, locale)
        headers = self._build_search_headers()
        response = self.query('search', url, headers=headers)
        return response

    def _response_to_json(self, api, response):
        return response.json()
