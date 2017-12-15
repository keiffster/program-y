"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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
from programy.extensions.base import Extension


class WeatherExtension(Extension):

    # WEATHER [OBSERVATION|FORECAST3|FORECAST24] LOCATION * WHEN *

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, bot, clientid, data):

        splits = data.split()
        if len(splits) != 5:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Weather - Not enough paramters passed, [%d] expected 5"%len(splits))
            return None

        type = splits[0]
        if type not in ['OBSERVATION', 'FORECAST3', 'FORECAST24']:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Weather - Type not understood [%s]"%type)
            return None

        if splits[1] == 'LOCATION':
            postcode = splits[2]
        else:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Weather - LOCATION missing")
            return None

        if splits[3] == 'WHEN':
            when = splits[4]
        else:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Weather - WHEN missing")
            return None

        if type == 'OBSERVATION':
            return self.get_observation(bot, clientid, postcode, when)
        elif type == 'FORECAST3':
            return self.get_forecast3(bot, clientid, postcode, when)
        elif type == 'FORECAST24':
            return self.get_forecast24(bot, clientid, postcode, when)

    def get_observation(self, bot, clientid, postcode, when):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Getting weather observation for [%s] at time [%s]"%(postcode, when))

        googlemaps = GoogleMaps(bot.license_keys)
        latlng = googlemaps.get_latlong_for_location(postcode)

        met_office = MetOffice(bot.license_keys)

        observation = met_office.current_observation(latlng.latitude, latlng.longitude)
        if observation is not None:
            return observation.get_latest().to_program_y_text()
        else:
            return None

    def get_forecast3(self, bot, clientid, postcode, when):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Getting 3 hourly weather forecast for [%s] at time [%s]"%(postcode, when))

        googlemaps = GoogleMaps(bot.license_keys)
        latlng = googlemaps.get_latlong_for_location(postcode)

        met_office = MetOffice(bot.license_keys)

        forecast = met_office.three_hourly_forecast(latlng.latitude, latlng.longitude)
        if forecast is not None:
            return forecast.get_latest().to_program_y_text()
        else:
            return None

    def get_forecast24(self, bot, clientid, postcode, when):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Getting 24 hour weather forecast for [%s] at time [%s]"%(postcode, when))

        googlemaps = GoogleMaps(bot.license_keys)
        latlng = googlemaps.get_latlong_for_location(postcode)

        met_office = MetOffice(bot.license_keys)

        forecast = met_office.daily_forecast(latlng.latitude, latlng.longitude)
        if forecast is not None:
            return forecast.get_latest().to_program_y_text()
        else:
            return None

