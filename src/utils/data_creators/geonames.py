import os

from programy.utils.text.text import TextUtils
from programy.utils.geo.geonames import GeoNamesApi
from programy.utils.license.keys import LicenseKeys

if __name__ == '__main__':

    # Only to be used to create test data for unit aiml_tests

    license_keys = LicenseKeys()
    license_keys.load_license_key_file(os.path.dirname(__file__) + TextUtils.replace_path_seperator('/../../../../bots/y-bot/config/license.keys'))

    geonamesapi = GeoNamesApi(license_keys)

    # Running these tools drops test files into the geocode test folder
    geonamesapi.store_get_latlong_for_postcode_to_file("KY39UR", TextUtils.replace_path_seperator("../../../test/utils/geocode/geonames_latlong.json"))
    geonamesapi.store_get_latlong_for_postcode_to_file("KY39UR", TextUtils.replace_path_seperator("../../../test/utils/geo/geonames_latlong.json"))

    # Only to be used to create test data for unit aiml_tests

