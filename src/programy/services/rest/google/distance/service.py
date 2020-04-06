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


class GoogleDistanceServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GoogleDistanceServiceQuery(service)

    def parse_matched(self, matched):
        self._origin = ServiceQuery._get_matched_var(matched, 0, "origin")
        self._destination = ServiceQuery._get_matched_var(matched, 1, "destination")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._origin = None
        self._destination = None

    def execute(self):
        return self._service.get_distance(self._origin, self._destination)

    def aiml_response(self, response):
        payload = response['response']['payload']
        rows = payload['rows']
        elements = rows[0]['elements']
        distance = elements[0]['distance']
        result = distance['text']
        YLogger.debug(self, result)
        return result


class GoogleDistanceServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class GoogleDistanceService(RESTService):
    """
    """
    PATTERNS = [
        [r"DISTANCE\sORIGIN\s(.+)\DESTINATION\s(.+)", GoogleDistanceServiceQuery]
    ]

    DISTANCE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}" \
                   "&region={2}&units={3}&key={4}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return GoogleDistanceService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('GOOGLE_MAPS')
        if self._api_key is None:
            YLogger.error(self, "GOOGLE_MAPS missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "distance.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "distance.conf"

    def _build_distance_url(self, origin, destination, region, units):
        url = GoogleDistanceService.DISTANCE_URL.format(origin, destination, region, units, self._api_key)
        return url

    def get_distance(self, origin, destination, region="uk", units="imperial"):
        url = self._build_distance_url(origin, destination, region, units)
        response =  self.query('get_distance', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

