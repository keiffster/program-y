import os

from programy.utils.text.text import TextUtils
from programy.utils.geo.google import GoogleMaps
from programy.utils.license.keys import LicenseKeys

if __name__ == '__main__':

    license_keys = LicenseKeys()
    license_keys.load_license_key_file(os.path.dirname(__file__) + TextUtils.replace_path_seperator('/../../../../bots/y-bot/config/license.keys'))

    # Only to be used to create test data for unit aiml_tests
    googlemaps = GoogleMaps(license_keys)

    # Running these tools drops test files into the geocode test folder
    googlemaps.store_get_latlong_for_location_to_file("KY3 9UR", TextUtils.replace_path_seperator(
        "../../../test/utils/geo/google_latlong.json"))
    googlemaps.store_get_distance_between_addresses_as_file("Edinburgh", "Kinghorn", TextUtils.replace_path_seperator(
        "../../../test/utils/geo/distance.json"))
    googlemaps.store_get_directions_between_addresses_as_file("Edinburgh", "Kinghorn", TextUtils.replace_path_seperator(
        "../../../test/utils/geo/directions.json"))

    googlemaps.store_get_latlong_for_location_to_file("KY3 9UR", TextUtils.replace_path_seperator(
        "../../../test/utils/weather/google_latlong.json"))
    googlemaps.store_get_distance_between_addresses_as_file("Edinburgh", "Kinghorn", TextUtils.replace_path_seperator(
        "../../../test/utils/weather/distance.json"))
    googlemaps.store_get_directions_between_addresses_as_file("Edinburgh", "Kinghorn", TextUtils.replace_path_seperator(
        "../../../test/utils/weather/directions.json"))
    # Only to be used to create test data for unit aiml_tests
