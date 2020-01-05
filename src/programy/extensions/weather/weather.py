"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from programy.utils.weather.metoffice import MetOffice
from programy.utils.weather.metoffice import MetOffice5DayForecast
from programy.utils.weather.metoffice import MetOffice24HourForecast
from programy.utils.geo.google import GoogleMaps
from programy.extensions.base import Extension


class WeatherExtension(Extension):

    def get_geo_locator(self):
        return GoogleMaps()

    def get_met_office(self):
        return MetOffice()

    def get_from_date(self):
        return None

    # WEATHER [OBSERVATION|FORECAST3|FORECAST24] LOCATION * WHEN *

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):

        try:
            fromdate = self.get_from_date()

            splits = data.split()
            if len(splits) != 5:
                YLogger.debug(client_context, "Weather - Not enough paramters passed, [%d] expected 5", len(splits))
                return None

            obvtype = splits[0]
            if obvtype not in ['OBSERVATION', 'FORECAST5DAY', 'FORECAST24HOUR']:
                YLogger.debug(client_context, "Weather - Type not understood [%s]", obvtype)
                return None

            if splits[1] == 'LOCATION':
                postcode = splits[2]
            else:
                YLogger.debug(client_context, "Weather - LOCATION missing")
                return None

            if splits[3] == 'WHEN':
                when = splits[4]
            else:
                YLogger.debug(client_context, "Weather - WHEN missing")
                return None

            if obvtype == 'OBSERVATION':
                result = self.current_observation(client_context, postcode)

            elif obvtype == 'FORECAST5DAY':
                result =  self.five_day_forecast(client_context, postcode, when, fromdate=fromdate)

            else: # obvtype == 'FORECAST24HOUR':
                result = self.twentyfour_hour_forecast(client_context, postcode, when, fromdate=fromdate)

            return result

        except Exception as error:
            YLogger.exception(client_context, "Failed to execute weather extension", error)

        return "UNAVAILABLE"

    def current_observation(self, context, postcode):
        YLogger.debug(context, "Getting weather observation for [%s]", postcode)

        googlemaps = self.get_geo_locator()
        latlng = googlemaps.get_latlong_for_location(postcode)

        met_office = self.get_met_office()

        observation = met_office.current_observation(latlng.latitude, latlng.longitude)
        if observation is not None:
            return observation.get_latest_observation().to_program_y_text()
        else:
            return "UNAVAILABLE"

    def twentyfour_hour_forecast(self, context, postcode, when, fromdate=None):
        YLogger.debug(context, "Getting 24 hour weather forecast for [%s] at time [%s]", postcode, when)

        googlemaps = self.get_geo_locator()
        latlng = googlemaps.get_latlong_for_location(postcode)

        met_office = self.get_met_office()

        forecast = met_office.twentyfour_hour_forecast(latlng.latitude, latlng.longitude)
        if forecast is not None:

            datapoint = forecast.get_forecast_for_n_hours_ahead(int(when), fromdate=fromdate)
            if datapoint is not None:
                return datapoint

            datapoint = forecast.get_latest_forecast().to_program_y_text()
            if datapoint is not None:
                return datapoint

        return "UNAVAILABLE"

    def five_day_forecast(self, context, postcode, when, fromdate=None):
        YLogger.debug(context, "Getting 5 day forecast for [%s] at time [%s]", postcode, when)

        googlemaps = self.get_geo_locator()
        latlng = googlemaps.get_latlong_for_location(postcode)

        met_office = self.get_met_office()

        forecast = met_office.five_day_forecast(latlng.latitude, latlng.longitude)
        if forecast is not None:

            datapoint = forecast.get_forecast_for_n_days_ahead(int(when), fromdate=fromdate)
            if datapoint is not None:
                return datapoint

            datapoint = forecast.get_latest_forecast().to_program_y_text()
            if datapoint is not None:
                return datapoint

        return "UNAVAILABLE"
