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

import json
import urllib.request
from programy.utils.logging.ylogger import YLogger
from programy.utils.geo.latlong import LatLong


class GeoNamesApi:
    POSTALCODESEARCH = "http://api.geonames.org/postalCodeSearchJSON?postalcode={0}&country={1}&maxRows=10&username={2}"

    def __init__(self):
        self.latlong_response_file = None
        self.account_name = None
        self.country = None

    def check_for_license_keys(self, license_keys):

        if license_keys.has_key('GEO_NAMES_ACCOUNTNAME'):
            self.account_name = license_keys.get_key('GEO_NAMES_ACCOUNTNAME')
        else:
            raise Exception("No valid license key GEO_NAMES_ACCOUNTNAME")

        if license_keys.has_key('GEO_NAMES_COUNTRY'):
            self.country = license_keys.get_key('GEO_NAMES_COUNTRY')
        else:
            raise Exception("No valid license key GEO_NAMES_COUNTRY")

    def _format_postcode(self, postcode):
        return "".join(postcode.split(" "))

    def _format_url(self, postcode):
        postcode = self._format_postcode(postcode)
        return GeoNamesApi.POSTALCODESEARCH.format(postcode, self.country, self.account_name)

    def _get_latlong_for_postcode_response(self, url):

        response = urllib.request.urlopen(url)                          # pragma: no cover
        if response is None:                                            # pragma: no cover
            raise Exception("Invalid url: ", url)                       # pragma: no cover

        content = response.read()                                       # pragma: no cover
        if response is None:                                            # pragma: no cover
            raise Exception("Invalid response from GeoNames")           # pragma: no cover

        return json.loads(content.decode('utf8'))                       # pragma: no cover

    def get_latlong_for_postcode(self, postcode):

        url = self._format_url(postcode)

        data = self._get_latlong_for_postcode_response(url)

        if 'postalCodes' not in data:
            raise Exception("Invalid/Unknown post code")

        if not data['postalCodes']:
            raise Exception("Invalid/Unknown post code")

        if 'lat' not in data['postalCodes'][0] or 'lng' not in data['postalCodes'][0]:
            raise Exception("Invalid/Unknown post code")

        return LatLong(data['postalCodes'][0]['lat'], data['postalCodes'][0]['lng'])
