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
import metoffer
from datetime import datetime
from programy.services.library.metoffice.metoffice import MetOffice
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.library.base import PythonAPIService
from programy.services.utils.geocode import GeoCodeUtils


class MetOfficeObservationQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return MetOfficeObservationQuery(service)

    def parse_matched(self, matched):
        latsign = ServiceQuery._get_matched_var(matched, 0, "latsign")
        latdec = ServiceQuery._get_matched_var(matched, 1, "latdec")
        latfrac = ServiceQuery._get_matched_var(matched, 2, "latfrac")
        self._lat = GeoCodeUtils.aiml_string_to_float(latsign, latdec, latfrac)

        lngsign = ServiceQuery._get_matched_var(matched, 3, "lngsign")
        lngdec = ServiceQuery._get_matched_var(matched, 4, "lngdec")
        lngfrac = ServiceQuery._get_matched_var(matched, 5, "lngfrac")
        self._lng = GeoCodeUtils.aiml_string_to_float(lngsign, lngdec, lngfrac)

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._lat = None
        self._lng = None

    def execute(self):
        return self._service.observation(self._lat, self._lng)

    def aiml_response(self, response):
        observation = MetOffice.parse_observation(response['response']['payload']['observation'])
        current = observation.get_latest_observation()
        result = current.to_program_y_text()
        YLogger.debug(self, result)
        return result


class MetOfficeHoursForecastQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return MetOfficeHoursForecastQuery(service)

    def parse_matched(self, matched):
        latsign = ServiceQuery._get_matched_var(matched, 0, "latsign")
        latdec = ServiceQuery._get_matched_var(matched, 1, "latdec")
        latfrac = ServiceQuery._get_matched_var(matched, 2, "latfrac")
        self._lat = GeoCodeUtils.aiml_string_to_float(latsign, latdec, latfrac)

        lngsign = ServiceQuery._get_matched_var(matched, 3, "lngsign")
        lngdec = ServiceQuery._get_matched_var(matched, 4, "lngdec")
        lngfrac = ServiceQuery._get_matched_var(matched, 5, "lngfrac")
        self._lng = GeoCodeUtils.aiml_string_to_float(lngsign, lngdec, lngfrac)

        self._hours = int(ServiceQuery._get_matched_var(matched, 6, "hours"))

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._lat = None
        self._lng = None
        self._hours = None

    def execute(self):
        return self._service.forecast(self._lat, self._lng, metoffer.THREE_HOURLY)

    def _get_current_date(self):
        time_now = datetime.now()
        return time_now.strftime("%Y-%m-%dZ")

    def aiml_response(self, response):
        forecasts = MetOffice.parse_forecast(response['response']['payload']['forecast'], metoffer.THREE_HOURLY)
        forecast = forecasts.get_forecast_for_n_hours_ahead(self._hours, fromdate=self._get_current_date())
        YLogger.debug(self, forecast)
        return forecast


class MetOfficeDaysForecastQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return MetOfficeDaysForecastQuery(service)

    def parse_matched(self, matched):
        latsign = ServiceQuery._get_matched_var(matched, 0, "latsign")
        latdec = ServiceQuery._get_matched_var(matched, 1, "latdec")
        latfrac = ServiceQuery._get_matched_var(matched, 2, "latfrac")
        self._lat = GeoCodeUtils.aiml_string_to_float(latsign, latdec, latfrac)

        lngsign = ServiceQuery._get_matched_var(matched, 3, "lngsign")
        lngdec = ServiceQuery._get_matched_var(matched, 4, "lngdec")
        lngfrac = ServiceQuery._get_matched_var(matched, 5, "lngfrac")
        self._lng = GeoCodeUtils.aiml_string_to_float(lngsign, lngdec, lngfrac)

        self._days = int(ServiceQuery._get_matched_var(matched, 6, "days"))

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._lat = None
        self._lng = None
        self._days = None

    def execute(self):
        return self._service.forecast(self._lat, self._lng, metoffer.DAILY)

    def _get_current_date(self):
        time_now = datetime.now()
        return time_now.strftime("%Y-%m-%dZ")

    def aiml_response(self, response):
        forecasts = MetOffice.parse_forecast(response['response']['payload']['forecast'], metoffer.DAILY)
        forecast = forecasts.get_forecast_for_n_days_ahead(self._days, fromdate=self._get_current_date())
        YLogger.debug(self, forecast)
        return forecast


class MetOfficeService(PythonAPIService):

    PATTERNS = [
        [r"OBSERVATION\sLAT\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sLNG\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)", MetOfficeObservationQuery],
        [r"FORECAST\sLAT\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sLNG\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sHOURS\s(.+)", MetOfficeHoursForecastQuery],
        [r"FORECAST\sLAT\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sLNG\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sDAYS\s(.+)", MetOfficeDaysForecastQuery]
    ]

    def __init__(self, configuration):
        PythonAPIService.__init__(self, configuration)
        self._met_office = None

    def patterns(self) -> list:
        return MetOfficeService.PATTERNS

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "metoffice.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "metoffice.conf"

    def _response_to_json(self, api, response):
        return response

    def initialise(self, client):
        self._api_key = client.license_keys.get_key("METOFFICE_API_KEY")
        if self._api_key is None:
            YLogger.error(self, "METOFFICE_API_KEY missing from license.keys, service will not function correctly!")
        self._met_office = MetOffice(self._api_key)

    def observation(self, lat, long):
        started = datetime.now()
        speed = None
        try:
            data = self._met_office.current_observation(lat, long)
            speed = started - datetime.now()

            if data is not None:
                result = {"observation": data}
                return self._create_success_payload("observation", started, speed, result)

            return self._create_failure_payload("observation", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("observation", started, speed, error)

    def forecast(self, lat, long, forecast):
        started = datetime.now()
        speed = None
        try:
            if forecast == metoffer.DAILY:
                data = self._met_office.five_day_forecast(lat, long)

            elif forecast == metoffer.THREE_HOURLY:
                data = self._met_office.twentyfour_hour_forecast(lat, long)

            else:
                raise ValueError("Invalid forecast type")

            speed = started - datetime.now()

            if data is not None:
                result = {"forecast": data}
                return self._create_success_payload("forecast", started, speed, result)

            return self._create_failure_payload("forecast", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("forecast", started, speed, error)

