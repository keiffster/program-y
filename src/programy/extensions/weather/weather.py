"""
Copyright (c) 2016 Keith Sterling

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

import logging

from programy.utils.weather.metoffice import MetOffice
from programy.utils.geo.google import GoogleMaps

class WeatherExtension(object):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, bot, clientid, data):

        splits = data.split()

        if splits[0] == 'LOCATION':
            postcode = splits[1]
        else:
            return None

        if splits[2] == 'WHEN':
            when = splits[3]
        else:
            return None

        logging.debug("Getting weather for %s at time %s"%(postcode, when))

        googlemaps = GoogleMaps(bot.license_keys)
        latlng = googlemaps.get_latlong_for_location(postcode)

        logging.debug ("Weather - Calling external weather service for with extra data [%s]"%(data))

        met_office = MetOffice(bot.license_keys)

        observation = met_office.current_observation(latlng.latitude, latlng.longitude)

        return observation.get_latest().to_program_y_text()
