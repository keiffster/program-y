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


class GoogleDirectionsServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GoogleDirectionsServiceQuery(service)

    def parse_matched(self, matched):
        self._origin = ServiceQuery._get_matched_var(matched, 0, "origin")
        self._destination = ServiceQuery._get_matched_var(matched, 1, "destination")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._origin = None
        self._destination = None

    def execute(self):
        return self._service.get_directions(self._origin, self._destination)

    def aiml_response(self, response):
        payload = response['response']['payload']
        routes = payload['routes']
        legs = routes[0]['legs']
        steps = legs[0]['steps']
        instructions = [step['html_instructions'] for step in steps]
        alist = ["<li>{0}</li>\n".format(instruction) for instruction in instructions]
        result = "<ol>{0}</ol>".format("".join(alist))
        YLogger.debug(self, result)
        return result


class GoogleDirectionsServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class GoogleDirectionsService(RESTService):
    """
    """
    PATTERNS = [
        [r"DIRECTIONS\sORIGIN\s(.+)\DESTINATION\s(.+)", GoogleDirectionsServiceQuery]
    ]

    MODES = [
        "DRIVING",
        "WALKING",
        "BICYCLING"
    ]

    DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}" \
                     "&region={2}&mode={3}&units={4}&key={5}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return GoogleDirectionsService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('GOOGLE_MAPS')
        if self._api_key is None:
            YLogger.error(self, "GOOGLE_MAPS missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "directions.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "directions.conf"

    def _build_directions_url(self, origin, destination, region, mode, units):
        url = GoogleDirectionsService.DIRECTIONS_URL.format(origin, destination, region, mode, units, self._api_key)
        return url

    def get_directions(self, origin, destination, region="uk", mode="DRIVING", units="imperial"):
        url = self._build_directions_url(origin, destination, region, mode, units)
        response = self.query('get_directions', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

