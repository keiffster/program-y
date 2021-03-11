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
import urllib.parse
import os
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class AccuWeatherPostCodeSearchServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return AccuWeatherTextSearchServiceQuery(service)

    def parse_matched(self, matched):
        self._postcode = ServiceQuery._get_matched_var(matched, 0, "postcode")
        self._country = ServiceQuery._get_matched_var(matched, 1, "country", optional=True)

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._postcode = None
        self._country = None

    def execute(self):
        return self._service.postcodesearch(self._postcode, self._country)

    def aiml_response(self, response):
        result = "KEY {0}".format(AccuWeatherService.get_location_key(response))
        YLogger.debug(self, result)
        return result


class AccuWeatherTextSearchServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return AccuWeatherTextSearchServiceQuery(service)

    def parse_matched(self, matched):
        self._location = ServiceQuery._get_matched_var(matched, 0, "location")
        self._country = ServiceQuery._get_matched_var(matched, 1, "country", optional=True)

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._location = None
        self._country = None

    def execute(self):
        return self._service.textsearch(self._location, self._country)

    def aiml_response(self, response):
        result = "KEY {0}".format(AccuWeatherService.get_location_key(response))
        YLogger.debug(self, result)
        return result


class AccuWeatherConditionsServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return AccuWeatherConditionsServiceQuery(service)

    def parse_matched(self, matched):
        self._location = ServiceQuery._get_matched_var(matched, 0, "location")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._location = None

    def execute(self):
        return self._service.conditions(self._location)

    def aiml_response(self, response):
        try:
            payload = response['response']['payload'][0]
            result = "EPOC {0} WEATHERTEXT {1} HASPRECIPITATION {2} PRECIPITATIONTYPE {3} ISDAYTIME {4} TEMP {5} UNIT {6}".format(
                    payload['EpochTime'],
                    payload['WeatherText'],
                    payload['HasPrecipitation'],
                    payload['PrecipitationType'],
                    payload['IsDayTime'],
                    payload['Temperature']['Metric']['Value'],
                    payload['Temperature']['Metric']['Unit'])
            YLogger.debug(self, result)
            return result

        except Exception as error:
            YLogger.exception(self, "Failed to parse Accuweather response to AIML", error)

        return None


class AccuWeatherServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class AccuWeatherService(RESTService):
    """
    """
    PATTERNS = [
        [r"TEXTSEARCH\sLOCATION\s(.+)", AccuWeatherTextSearchServiceQuery],
        [r"CONDITIONS\sLOCATION\s(.+)", AccuWeatherConditionsServiceQuery]
    ]

    POSTCODESEARCH_BASE_URL="http://dataservice.accuweather.com/locations/v1/postalcodes/search"
    POSTCODESEARCH_COUNTRY_BASE_URL="http://dataservice.accuweather.com/locations/v1/postalcodes/{0}/search"
    TEXTSEARCH_BASE_URL="http://dataservice.accuweather.com/locations/v1/search"
    TEXTSEARCH_COUNTRY_BASE_URL="http://dataservice.accuweather.com/locations/v1/{0}/search"
    CONDITIONS_BASE_URL="http://dataservice.accuweather.com/currentconditions/v1/"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return AccuWeatherService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('ACCUWEATHER_APIKEY')
        if self._api_key is None:
            YLogger.error(self, "ACCUWEATHER_APIKEY missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "accuweather.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "accuweather.conf"

    def _build_postcodesearch_url(self, postcode, country, language=None, details=None, offset=None, alias=None):
        if country is None:
            url = AccuWeatherService.POSTCODESEARCH_BASE_URL
        else:
            url = AccuWeatherService.POSTCODESEARCH_COUNTRY_BASE_URL.format(country)
        url += "?apikey={0}".format(self._api_key)
        url += "&q={0}".format(postcode)
        if language is not None:
            url += "&language={0}".format(language)
        if details is not None:
            url += "&details={0}".format(details)
        if offset is not None:
            url += "&offset={0}".format(offset)
        if alias is not None:
            url += "&alias={0}".format(alias)
        return url

    def postcodesearch(self, postcode, country=None, language=None, details=None, offset=None, alias=None):
        url = self._build_postcodesearch_url(urllib.parse.quote_plus(postcode), country, language, details, offset, alias)
        response = self.query('postcodesearch', url)
        return response

    def _build_textsearch_url(self, postcode, country, language=None, details=None, offset=None, alias=None):
        if country is None:
            url = AccuWeatherService.TEXTSEARCH_BASE_URL
        else:
            url = AccuWeatherService.TEXTSEARCH_COUNTRY_BASE_URL.format(country)
        url += "?apikey={0}".format(self._api_key)
        url += "&q={0}".format(postcode)
        if language is not None:
            url += "&language={0}".format(language)
        if details is not None:
            url += "&details={0}".format(details)
        if offset is not None:
            url += "&offset={0}".format(offset)
        if alias is not None:
            url += "&alias={0}".format(alias)
        return url

    def textsearch(self, location, country=None, language=None, details=None, offset=None, alias=None):
        url = self._build_textsearch_url(urllib.parse.quote_plus(location), country, language, details, offset, alias)
        response = self.query('textsearch', url)
        return response

    def _build_conditions_url(self, location, language=None, details=None):
        url = AccuWeatherService.CONDITIONS_BASE_URL
        url += location
        url += "?apikey={0}".format(self._api_key)
        if language is not None:
            url += "&language={0}".format(language)
        if details is not None:
            url += "&details={0}".format(details)
        return url

    def conditions(self, location, language=None, details=None):
        url = self._build_conditions_url(location, language, details)
        response = self.query('conditions', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

    @staticmethod
    def get_location_key(data):
        response = data.get("response")
        if response is not None:
            payload = response.get("payload")
            if payload is not None:
                if len(payload) > 0:
                    payload0 = payload[0]
                    key = payload0.get("Key")
                    return key
        return None