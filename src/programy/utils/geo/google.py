"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger
import json
import urllib.request

from programy.utils.geo.latlong import LatLong
from programy.utils.text.text import TextUtils

class GoogleAddressComponent(object):
    def __init__(self):
        self.long_name = None
        self.short_name = None
        self.types = []

    def parse_json(self, data):
        self.long_name = data['long_name']
        self.short_name = data['short_name']
        self.types = []
        for address_type in data['types']:
            self.types.append(address_type)


class GoogleBounds(object):
    def __init__(self):
        self.northeast = None
        self.southwest = None

    def parse_json(self, data):
        self.northeast = LatLong(data['northeast']['lat'], data['northeast']['lng'])
        self.southwest = LatLong(data['southwest']['lat'], data['southwest']['lng'])


class GoogleGeometry(object):
    def __init__(self):
        self.location_type = None
        self.location = None
        self.bounds = None
        self.viewport = None

    def parse_json(self, data):
        self.location_type = data['location_type']
        self.location = LatLong(data['location']['lat'], data['location']['lng'])
        self.bounds = GoogleBounds()
        self.bounds.parse_json(data['bounds'])
        self.viewport = GoogleBounds()
        self.viewport.parse_json(data['bounds'])


class GoogleGeoLocation(object):
    def __init__(self):
        self.place_id = None
        self.formatted_address = None
        self.address_components = []
        self.geometry = None
        self.types = []

    def parse_json(self, data):
        self.place_id = data['place_id']
        self.formatted_address = data['formatted_address']

        self.address_components = []
        for component_data in data['address_components']:
            component = GoogleAddressComponent()
            component.parse_json(component_data)
            self.address_components.append(component)

        self.geometry = GoogleGeometry()
        self.geometry.parse_json(data['geometry'])

        self.types = []
        for type_data in data['types']:
            self.types.append(type_data)


class GoogelMapsResult(object):
    def __init__(self):
        self.locations = []
        self.status = None

    def parse_json(self, data):
        self.status = data['status']
        for result in data['results']:
            location = GoogleGeoLocation()
            location.parse_json(result)
            self.locations.append(location)


class GoogleDistance(object):
    def __init__(self, origin, destination, country="UK", mode="driving", units="imperial"):
        self._origin = origin
        self._destination = destination
        self._country = country
        self._mode = mode
        self._units = units

        self._distance = None
        self._distance_text = None
        self._duration = None
        self._duration_text = None

    @property
    def distance_text(self):
        return self._distance_text

    def parse_json(self, json_data):
        result = json_data[0]

        if 'elements' not in result:
            raise ValueError("Invalid json data array")

        if 'distance' not in result['elements'][0]:
            raise ValueError("Invalid json data array")

        self._distance = result['elements'][0]['distance']['value']
        self._distance_text = result['elements'][0]['distance']['text']

        if 'duration' not in result['elements'][0]:
            raise ValueError("Invalid json data array")

        self._duration = result['elements'][0]['duration']['value']
        self._duration_text = result['elements'][0]['duration']['text']


class DirectionLegStep(object):
    def __init__(self):
        self._distance = None
        self._distance_text = None
        self._duration = None
        self._duration_text = None
        self._instructions = None

    @property
    def instructions(self):
        return self._instructions

    def parse_json(self, data):
        self._distance = data['distance']['value']
        self._distance_text = data['distance']['text']
        self._duration = data['duration']['value']
        self._duration_text = data['duration']['text']
        self._instructions = TextUtils.strip_html(data['html_instructions'])


class DirectionLeg(object):
    def __init__(self):
        self._distance = None
        self._distance_text = None
        self._duration = None
        self._duration_text = None
        self._steps = []

    def parse_json(self, data):
        self._distance = data['distance']['value']
        self._distance_text = data['distance']['text']
        self._duration = data['duration']['value']
        self._duration_text = data['duration']['text']
        for step in data['steps']:
            dirlegstep = DirectionLegStep()
            dirlegstep.parse_json(step)
            self._steps.append(dirlegstep)

    def steps_as_a_string(self):
        return ", ".join([step.instructions for step in self._steps])


class GoogleDirections(object):
    def __init__(self, origin, destination, country="UK", mode="driving", units="imperial"):
        self._origin = origin
        self._destination = destination
        self._country = country
        self._mode = mode
        self._units = units
        self._legs = []

    def parse_json(self, routes):
        route = routes[0]
        for leg in route['legs']:
            dirleg = DirectionLeg()
            dirleg.parse_json(leg)
            self._legs.append(dirleg)

    def legs_as_a_string(self):
        return ", ".join([leg.steps_as_a_string() for leg in self._legs])


class GoogleMaps(object):

    DIRECTIONS = "http://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}" \
                 "&country={2}&sensor=false&mode={3}"
    DISTANCE = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}" \
               "&country={2}&sensor=false&mode={3}&units={4}"
    GEOCODE = "http://maps.google.com/maps/api/geocode/json?address={0}&sensor=false"

    ##################

    def _get_response_as_json(self, url):
        YLogger.debug(self, "GoogleMaps Request = [%s]", url)
        response = urllib.request.urlopen(url)
        content = response.read()
        decoded = content.decode('utf8')
        YLogger.debug(self, "GoogleMaps Response = [%s]", decoded)
        return json.loads(decoded)

    ##################

    def _get_latlong_for_location_response(self, location):
        location = TextUtils.urlify(location)
        url = GoogleMaps.GEOCODE.format(location)
        return self._get_response_as_json(url)

    def is_error_response(self, response):
        if 'status' in response:
            if response['status'] == 'OVER_QUERY_LIMIT' :
                return True
        return False

    def get_latlong_for_location(self, location):
        YLogger.debug(self, "get_latlong_for_location - calling service")
        response = self._get_latlong_for_location_response(location)

        if self.is_error_response(response):
            raise Exception(response['status'])

        geodata = GoogelMapsResult()
        geodata.parse_json(response)
        return geodata.locations[0].geometry.location

    ##################

    def _get_distance_between_addresses(self, origin, destination, country, mode, units):
        origin = TextUtils.urlify(origin)
        destination = TextUtils.urlify(destination)
        url = GoogleMaps.DISTANCE.format(origin, destination, country, mode, units)
        return self._get_response_as_json(url)

    def get_distance_between_addresses(self, origin, destination, country="UK", mode="driving", units="imperial"):
        YLogger.debug(self, "get_distance_between_addresses - calling service")
        response = self._get_distance_between_addresses(origin, destination, country, mode, units)

        if response['status'] == 'OK':
            YLogger.debug(self, "get_distance_between_addresses - OK")
            distance = GoogleDistance(origin, destination, country, mode, units)
            distance.parse_json(response['rows'])
            return distance
        else:
            YLogger.error(self, "get_distance_between_addresses - [%s]", response['status'])
            return None

    ##################

    def _get_directions_between_addresses_response(self, origin, destination, country, mode, units):
        origin = TextUtils.urlify(origin)
        destination = TextUtils.urlify(destination)
        url = GoogleMaps.DIRECTIONS.format(origin, destination, country, mode, units)
        return self._get_response_as_json(url)

    def get_directions_between_addresses(self, origin, destination, country="UK", mode="driving", units="imperial"):
        YLogger.debug(self, "get_directions_between_addresses - calling live service")
        response = self._get_directions_between_addresses_response(origin, destination, country, mode, units)

        if response['status'] == 'OK':
            YLogger.debug(self, "get_directions_between_addresses - OK")
            directions = GoogleDirections(origin, destination, country, mode, units)
            directions.parse_json(response['routes'])
            return directions
        else:
            YLogger.error(self, "get_directions_between_addresses - %s", response['status'])
            return None

