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


class YelpBusinessSearchQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return YelpBusinessSearchQuery(service)

    def parse_matched(self, matched):
        self._term = ServiceQuery._get_matched_var(matched, 0, "term")
        self._location = ServiceQuery._get_matched_var(matched, 1, "location")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._term = None
        self._location = None

    def execute(self):
        return self._service.search(self._term, self._location)

    def aiml_response(self, response):
        payload = response['response']['payload']
        businesses = payload['businesses']
        result = "<ul>\n"
        for business in businesses:
            details = "{0} - {1} - {2}".format(business['name'], ", ".join(business['location']['display_address']), business['phone'])
            result += "<li>{0}</li>\n".format(details)
        result += "<ul>"
        return result


class YelpBusinessSearchServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class YelpBusinessSearchService(RESTService):
    """
    https://www.yelp.co.uk/developers/documentation/v3/business_search
    """
    PATTERNS = [
        [r"BUSINESS\sSEARCH\s(.+)\sLOCATION\s(.+)", YelpBusinessSearchQuery]
    ]

    BUSINESS_SEARCH_URL="https://api.yelp.com/v3/businesses/search"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None
        
    def initialise(self, client):
        self._api_key = client.license_keys.get_key('YELP_API_KEY')
        if self._api_key is None:
            YLogger.error(self, "YELP_API_KEY missing from license.keys, service will not function correctly!")

    def patterns(self) -> list:
        return YelpBusinessSearchService.PATTERNS

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "business.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "business.conf"

    def _build_search_url(self, term, location, locale):
        url = YelpBusinessSearchService.BUSINESS_SEARCH_URL
        url += "?term={0}&location={1}&locale={2}".format(urllib.parse.quote(term), location, locale)
        return url

    def _build_search_headers(self):
        return {"Authorization": "Bearer {0}".format(self._api_key)}

    def search(self, term, location, locale="en_GB"):
        url = self._build_search_url(term, location, locale)
        headers = self._build_search_headers()
        response = self.query('search', url, headers=headers)
        return response

    def _response_to_json(self, api, response):
        return response.json()
