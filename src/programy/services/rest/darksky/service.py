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


class DarkSkyForecastServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return DarkSkyForecastServiceQuery(service)

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
        return self._service.forecast(self._lat, self._lng)

    def aiml_response(self, response):
        payload = response['response']['payload']
        currently = payload['currently']
        forecast = currently['summary']
        result = "FORECAST {0}".format(forecast)
        YLogger.debug(self, result)
        return result


class DarkSkyTimeMachineServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return DarkSkyTimeMachineServiceQuery(service)

    def parse_matched(self, matched):
        latsign = ServiceQuery._get_matched_var(matched, 0, "latsign")
        latdec = ServiceQuery._get_matched_var(matched, 1, "latdec")
        latfrac = ServiceQuery._get_matched_var(matched, 2, "latfrac")
        self._lat = GeoCodeUtils.aiml_string_to_float(latsign, latdec, latfrac)

        lngsign = ServiceQuery._get_matched_var(matched, 3, "lngsign")
        lngdec = ServiceQuery._get_matched_var(matched, 4, "lngdec")
        lngfrac = ServiceQuery._get_matched_var(matched, 5, "lngfrac")
        self._lng = GeoCodeUtils.aiml_string_to_float(lngsign, lngdec, lngfrac)

        self._time = ServiceQuery._get_matched_var(matched, 6, "time")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._lat = None
        self._lng = None
        self._time = None

    def execute(self):
        return self._service.timemachine(self._lat, self._lng, self._time)

    def aiml_response(self, response):
        payload = response['response']['payload']
        currently = payload['currently']

        temperature = currently['temperature']
        dewPoint = currently['dewPoint']
        humidity = currently['humidity']
        windSpeed = currently['windSpeed']
        cloudCover = currently['cloudCover']
        uvIndex = currently['uvIndex']


        result = "TIMEMACHINE TEMP {0} DEWPOINT {1} HUMIDITY {2} WINDSPEED {3} CLOUDCOVER {4} UVINDEX {5}".\
            format(temperature, dewPoint, humidity, windSpeed, cloudCover, uvIndex)

        YLogger.debug(self, result)
        return result


class DarkSkyServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class DarkSkyService(RESTService):
    """
    """
    PATTERNS = [
        [r"FORECAST\sLAT\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sLNG\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)", DarkSkyForecastServiceQuery],
        [r"TIMEMACHINE\sLAT\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sLNG\sSIGN\s(.+)\sDEC\s(.+)\sFRAC\s(.+)\sTIME\s(.+)", DarkSkyTimeMachineServiceQuery]
    ]

    FORECAST_BASE_URL = " https://api.darksky.net/forecast"
    TIMEMACHINE_BASE_URL = "https://api.darksky.net/forecast"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._secret_key = None

    def patterns(self) -> list:
        return DarkSkyService.PATTERNS

    def initialise(self, client):
        self._secret_key = client.license_keys.get_key('DARKSKY_SECRETKEY')
        if self._secret_key is None:
            YLogger.error(self, "DARKSKY_SECRETKEY missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "darksky.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "darksky.conf"

    def _question_or_ampersand(self, question):
        if question is False:
            return "?"
        else:
            return "&"

    def _build_forecast_url(self, lat, lng, exclude=None, extend=None, lang=None, units=None):
        url = DarkSkyService.FORECAST_BASE_URL
        url += "/{0}".format(self._secret_key)
        url += "/{0},{1}".format(lat, lng)
        question=False
        if exclude is not None:
            url += self._question_or_ampersand(question)
            question = True
            url += "exclude={0}".format(exclude)
        if extend is not None:
            url += self._question_or_ampersand(question)
            question = True
            url += "extend={0}".format(extend)
        if lang is not None:
            url += self._question_or_ampersand(question)
            question = True
            url += "lang={0}".format(lang)
        if units is not None:
            url += self._question_or_ampersand(question)
            url += "units={0}".format(units)

        return url

    def forecast(self, lat, lng, exclude=None, extend=None, lang=None, units=None):
        url = self._build_forecast_url(lat, lng, exclude, extend, lang, units)
        response = self.query('forecast', url)
        return response

    def _build_timemachine_url(self, lat, lng, time, exclude=None, lang=None, units=None):
        url = DarkSkyService.TIMEMACHINE_BASE_URL
        url += "/{0}".format(self._secret_key)
        url += "/{0},{1},{2}".format(lat, lng, time)
        question=False
        if exclude is not None:
            url += self._question_or_ampersand(question)
            question = True
            url += "exclude={0}".format(exclude)
        if lang is not None:
            url += self._question_or_ampersand(question)
            question = True
            url += "lang={0}".format(lang)
        if units is not None:
            url += self._question_or_ampersand(question)
            url += "units={0}".format(units)

        return url

    def timemachine(self, lat, lng, time, exclude=None, lang=None, units=None):
        url = self._build_timemachine_url(lat, lng, time, exclude, lang, units)
        response = self.query('timemachine', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

