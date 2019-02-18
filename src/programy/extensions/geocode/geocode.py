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


class GeoCodeExtension(Extension):

    def get_geo_locator(self):
        return  GoogleMaps()

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context, data):
        YLogger.debug(context, "GeoCode [%s]", data)

        words = data.split(" ")
        if words[0] == 'POSTCODE1':
            location = words[1]
        elif words[0] == 'POSTCODE2':
            location = words[1] + words[2]
        elif words[0] == 'LOCATION':
            location = " ".join(words[1:])
        else:
            return None

        googlemaps = self.get_geo_locator()

        latlng = googlemaps.get_latlong_for_location(location)
        if latlng is not None:
            str_lat = str(latlng.latitude)
            str_lng = str(latlng.longitude)

            lats = str_lat.split(".")
            lngs = str_lng.split(".")

            return "LATITUDE DEC %s FRAC %s LONGITUDE DEC %s FRAC %s"%(
                lats[0], lats[1],
                lngs[0], lngs[1]
            )

        return None
