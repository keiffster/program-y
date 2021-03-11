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
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException
from programy.services.utils.geocode import GeoCodeUtils


class GoogleLatLongPostCodeServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GoogleLatLongPostCodeServiceQuery(service)

    def parse_matched(self, matched):
        self._postcode = ServiceQuery._get_matched_var(matched, 0, "postcode")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._postcode = None

    def execute(self):
        return self._service.latlng_for_postcode(self._postcode)

    def aiml_response(self, response):
        payload = response['response']['payload']
        results = payload['results']
        result = results[0]
        geometry = result['geometry']
        location = geometry['location']

        lat = location['lat']
        lng = location['lng']

        latText = GeoCodeUtils.float_to_aiml_string(lat)
        lngText = GeoCodeUtils.float_to_aiml_string(lng)

        result = GeoCodeUtils.aiml_lat_lng(latText, lngText)
        YLogger.debug(self, result)
        return result


class GoogleGeoCodeServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class GoogleGeoCodeService(RESTService):
    """
    """
    PATTERNS = [
        [r"LATLNG\sPOSTCODE\s(.+)", GoogleLatLongPostCodeServiceQuery]
    ]

    LATLNG_FOR_POSTCODE = "https://maps.google.com/maps/api/geocode/json?address={0}&sensor=false&key={1}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return GoogleGeoCodeService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('GOOGLE_MAPS')
        if self._api_key is None:
            YLogger.error(self, "GOOGLE_MAPS missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "geocode.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "geocode.conf"

    def _build_postcode_url(self, postcode):
        url = GoogleGeoCodeService.LATLNG_FOR_POSTCODE.format(postcode, self._api_key)
        return url

    def latlng_for_postcode(self, postcode):
        url = self._build_postcode_url(postcode)
        response = self.query('latlng_for_postcode', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

