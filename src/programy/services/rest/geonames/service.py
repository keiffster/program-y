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
import os
import urllib.parse
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException
from programy.services.utils.geocode import GeoCodeUtils


class GeoNamesLatLongPostCode(ServiceQuery):

    @staticmethod
    def create(service):
        return GeoNamesLatLongPostCode(service)

    def parse_matched(self, matched):
        self._postcode = ServiceQuery._get_matched_var(matched, 0, "postcode")
        self._country = ServiceQuery._get_matched_var(matched, 1, "country", True)
        if self._country is None:
            self._country = "uk"

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._postcode = None
        self._country = None

    def execute(self):
        return self._service.latlng_for_postcode(self._postcode, self._country)

    def aiml_response(self, response):
        payload = response['response']['payload']
        postalCodes = payload['postalCodes']
        lat = postalCodes[0]['lat']
        lng = postalCodes[0]['lng']

        latText = GeoCodeUtils.float_to_aiml_string(lat)
        lngText = GeoCodeUtils.float_to_aiml_string(lng)

        result = GeoCodeUtils.aiml_lat_lng(latText, lngText)
        YLogger.debug(self, result)
        return result


class GeoNamesPlacenamePostCode(ServiceQuery):

    @staticmethod
    def create(service):
        return GeoNamesPlacenamePostCode(service)

    def parse_matched(self, matched):
        self._placename = ServiceQuery._get_matched_var(matched, 0, "placename")
        self._country = ServiceQuery._get_matched_var(matched, 1, "country", True)
        if self._country is None:
            self._country = "uk"
        #else:
        #    self._country = self._country.lower()

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._placename = None
        self._country = None

    def execute(self):
        return self._service.latlng_for_placename(self._placename, self._country)

    def aiml_response(self, response):
        payload = response['response']['payload']
        postalCodes = payload['postalCodes']
        lat = postalCodes[0]['lat']
        lng = postalCodes[0]['lng']

        latText = GeoCodeUtils.float_to_aiml_string(lat)
        lngText = GeoCodeUtils.float_to_aiml_string(lng)

        result = GeoCodeUtils.aiml_lat_lng(latText, lngText)
        YLogger.debug(self, result)
        return result


class GeoNamesServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class GeoNamesService(RESTService):
    """
    https://gnews.io/docs/v3#introduction
    """
    PATTERNS = [
        [r"LATLNG\sPOSTCODE\s(\w+)", GeoNamesLatLongPostCode],
        [r"LATLNG\sPLACENAME\s(\w+)(?:\sCOUNTRY\s(\w+))?", GeoNamesPlacenamePostCode]
    ]

    POSTAL_CODE_SEARCH = "http://api.geonames.org/postalCodeSearchJSON?postalcode={0}&country={1}&maxRows=10&username={2}"
    PLACE_NAME_SEARCH = "http://api.geonames.org/postalCodeSearchJSON?placename={0}&country={1}&maxRows=10&username={2}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._account_name = None
        self._country = None

    def patterns(self) -> list:
        return GeoNamesService.PATTERNS

    def initialise(self, client):
        self._account_name = client.license_keys.get_key('GEO_NAMES_ACCOUNTNAME')
        if self._account_name is None:
            YLogger.error(self, "GEO_NAMES_ACCOUNTNAME missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "geonames.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "geonames.conf"

    def _build_postcode_url(self, postcode, country):
        url = GeoNamesService.POSTAL_CODE_SEARCH.format(urllib.parse.quote(postcode), urllib.parse.quote(country), self._account_name)
        return url

    def latlng_for_postcode(self, postcode, country='uk'):
        url = self._build_postcode_url(postcode, country)
        response = self.query('latlng_for_postcode', url)
        return response

    def _build_placename_url(self, placename, country):
        url = GeoNamesService.PLACE_NAME_SEARCH.format(urllib.parse.quote(placename), urllib.parse.quote(country), self._account_name)
        return url

    def latlng_for_placename(self, placename, country='uk'):
        url = self._build_placename_url(placename, country)
        response = self.query('latlng_for_placename', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

