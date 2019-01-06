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

from programy.utils.geo.google import GoogleMaps
from programy.extensions.base import Extension


class GoogleMapsExtension(Extension):

    def get_geo_locator(self):
        return GoogleMaps()

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context, data):
        YLogger.debug(context, "GoogleMaps [%s]", data)

        splits = data.split(" ")
        command = splits[0]
        from_place = splits[1]
        to_place = splits[2]

        googlemaps = self.get_geo_locator()

        if command == "DISTANCE":
            distance = googlemaps.get_distance_between_addresses(from_place, to_place)
            return self._format_distance_for_programy(distance)
        elif command == "DIRECTIONS":
            directions = googlemaps.get_directions_between_addresses(from_place, to_place)
            return self._format_directions_for_programy(directions)
        else:
            YLogger.error(context, "Unknown Google Maps Extension command [%s]", command)
            return None

    def _format_distance_for_programy(self, distance):
        distance_splits = distance.distance_text.split(" ")
        value = distance_splits[0]
        if "." in value:
            value_splits = distance_splits[0].split(".")
            dec = value_splits[0]
            frac = value_splits[1]
        else:
            dec = value
            frac = "0"
        units = distance_splits[1]
        if units == 'mi':
            units = "miles"
        return "DISTANCE DEC %s FRAC %s UNITS %s"%(dec, frac, units)

    def _format_directions_for_programy(self, directions):
        return "DIRECTIONS %s"%directions.legs_as_a_string()
