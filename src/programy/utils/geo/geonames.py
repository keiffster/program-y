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

import json
import urllib.request
from programy.utils.logging.ylogger import YLogger
from programy.utils.geo.latlong import LatLong


class GeoNamesApi(object):

    POSTALCODESEARCH = "http://api.geonames.org/postalCodeSearchJSON?postalcode={0}&country={1}&maxRows=10&username={2}"
    get_latlong_for_postcode_response_file = None

    def check_for_license_keys(self, license_keys):

        if license_keys.has_key('GEO_NAMES_ACCOUNTNAME'):
            self.account_name = license_keys.get_key('GEO_NAMES_ACCOUNTNAME')
        else:
            raise Exception("No valid license key GEO_NAMES_ACCOUNTNAME")

        if license_keys.has_key('GEO_NAMES_COUNTRY'):
            self.country = license_keys.get_key('GEO_NAMES_COUNTRY')
        else:
            raise Exception("No valid license key GEO_NAMES_COUNTRY")

        self.latlong_response_file = None
        if license_keys.has_key('GEONAMES_LATLONG'):
            self.country = license_keys.get_key('GEONAMES_LATLONG')


    def _get_latlong_for_postcode_response(self, postcode):

        if self.latlong_response_file is not None:
            return self.load_get_latlong_for_postcode_from_file(self.latlong_response_file)

        postcode = "".join(postcode.split(" "))
        url = GeoNamesApi.POSTALCODESEARCH.format(postcode, self.country, self.account_name)

        response = urllib.request.urlopen(url)
        if response is None:
            raise Exception("Invalid url: ", url)

        content = response.read()
        if response is None:
            raise Exception("Invalid response from GeoNames")

        return json.loads(content.decode('utf8'))

    def load_get_latlong_for_postcode_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as response_file:
                return json.load(response_file)

        except FileNotFoundError:
            YLogger.error(self, "File not found [%s]", filename)

    def store_get_latlong_for_postcode_to_file(self, postcode, filename):
        content = self._get_latlong_for_postcode_response(postcode)
        try:
            with open(filename, "w+", encoding="utf-8") as response_file:
                json.dump(content, response_file, sort_keys=True, indent=2)

        except FileNotFoundError:
            YLogger.error(self, "Failed to write to [%s]", filename)

    def get_latlong_for_postcode(self, postcode):

        if GeoNamesApi.get_latlong_for_postcode_response_file is None:
            data = self._get_latlong_for_postcode_response(postcode)
        else:
            try:
                with open(GeoNamesApi.get_latlong_for_postcode_response_file, "r", encoding="utf-8") as datafile:
                    data = json.load(datafile)
            except FileNotFoundError:
                YLogger.error(self, "File not found [%s]", GeoNamesApi.get_latlong_for_postcode_response_file)

        if 'postalCodes' not in data:
            raise Exception("Invalid/Unknown post code")
        if not data['postalCodes']:
            raise Exception("Invalid/Unknown post code")
        if 'lat' not in data['postalCodes'][0] or 'lng' not in data['postalCodes'][0]:
            raise Exception("Invalid/Unknown post code")

        return LatLong(data['postalCodes'][0]['lat'], data['postalCodes'][0]['lng'])
