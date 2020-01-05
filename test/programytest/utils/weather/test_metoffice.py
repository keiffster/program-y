import unittest
import metoffer
from programy.utils.weather.metoffice import MetOffice
from programytest.client import TestClient
from programytest.utils.weather.payloads.forecast_3hourly import forecast_3hourly_payload
from programytest.utils.weather.payloads.observation import observation_payload
from programytest.utils.weather.payloads.forecast_daily import forecast_daily_payload
from programy.utils.license.keys import LicenseKeys


class MockMetOffice(MetOffice):

    def __init__(self, license_keys, observation=None, forecast=None):
        MetOffice.__init__(self)
        self._license_keys = license_keys
        self._observation = observation
        self._forecast = forecast

    def get_forecast_data(self, lat, lon, forecast_type):
        return self._forecast

    def get_observation_data(self, lat, lon):
        return self._observation


class MetOfficeTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        self.lat = 56.0720397
        self.lng = -3.1752001

    def test_init_with_license_keys(self):
        met_office = MetOffice()
        self.assertIsNotNone(met_office)
        license_keys = LicenseKeys()
        license_keys.add_key('METOFFICE_API_KEY', "ABCDEFGHIJKL")
        met_office.check_for_license_keys(license_keys)
        self.assertIsNotNone(met_office._met_office_api)

    def test_init_with_license_keys_none_present(self):
        met_office = MetOffice()
        self.assertIsNotNone(met_office)
        license_keys = LicenseKeys()
        with self.assertRaises(Exception):
            met_office.check_for_license_keys(license_keys)

    def test_init_no_license_keys(self):
        self._client.license_keys.empty()
        with self.assertRaises(Exception):
            met_office = MetOffice()
            met_office.check_for_license_keys(None)

    def test_get_forecast_data_3hourly(self):
        met_office = MockMetOffice(self._client.license_keys, forecast=forecast_3hourly_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.get_forecast_data(self.lat, self.lng, metoffer.THREE_HOURLY)
        self.assertIsNotNone(forecast)

    def test_get_forecast_data_daily(self):
        met_office = MockMetOffice(self._client.license_keys, forecast=forecast_daily_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.get_forecast_data(self.lat, self.lng, metoffer.DAILY)
        self.assertIsNotNone(forecast)

    def test_get_observation_data(self):
        met_office = MockMetOffice(self._client.license_keys,  observation=observation_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.get_observation_data(self.lat, self.lng)
        self.assertIsNotNone(forecast)

    def test_nearest_location_forecast_3hourly(self):
        met_office = MockMetOffice(self._client.license_keys, forecast=forecast_3hourly_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.nearest_location_forecast(self.lat, self.lng, metoffer.THREE_HOURLY)
        self.assertIsNotNone(forecast)

    def test_nearest_location_forecast_daily(self):
        met_office = MockMetOffice(self._client.license_keys, forecast=forecast_daily_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.nearest_location_forecast(self.lat, self.lng, metoffer.DAILY)
        self.assertIsNotNone(forecast)

    def test_nearest_location_forecast_other(self):
        met_office = MockMetOffice(self._client.license_keys, forecast=forecast_daily_payload)
        self.assertIsNotNone(met_office)
        with self.assertRaises(ValueError):
            _ = met_office.nearest_location_forecast(self.lat, self.lng, "other")

    def test_observation(self):
        met_office = MockMetOffice(self._client.license_keys, observation=observation_payload)
        self.assertIsNotNone(met_office)

        observation = met_office.current_observation(self.lat, self.lng)
        self.assertIsNotNone(observation)

    def tes_five_day_forecast(self):
        met_office = MockMetOffice(self._client.license_keys, forecast=forecast_3hourly_payload)
        self.assertIsNotNone(met_office)

        forecast = met_office.five_day_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)

    def tets_twentyfour_hour_forecast(self):
        met_office = MockMetOffice(self._client.license_keys, forecast=forecast_daily_payload)
        self.assertIsNotNone(met_office)

        forecast = met_office.twentyfour_hour_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)


