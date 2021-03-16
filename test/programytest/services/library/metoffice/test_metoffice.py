import unittest
import metoffer
from programy.services.library.metoffice.metoffice import MetOffice
from programytest.client import TestClient
from programytest.services.library.metoffice.payloads.forecast_3hourly import forecast_3hourly_payload
from programytest.services.library.metoffice.payloads.observation import observation_payload
from programytest.services.library.metoffice.payloads.forecast_daily import forecast_daily_payload


class MockMetOffice(MetOffice):

    def __init__(self, api_key, observation=None, forecast=None):
        MetOffice.__init__(self, api_key)
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

    def test_get_forecast_data_3hourly(self):
        met_office = MockMetOffice("ABCDEFGHIJKL", forecast=forecast_3hourly_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.get_forecast_data(self.lat, self.lng, metoffer.THREE_HOURLY)
        self.assertIsNotNone(forecast)

    def test_get_forecast_data_daily(self):
        met_office = MockMetOffice("ABCDEFGHIJKL", forecast=forecast_daily_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.get_forecast_data(self.lat, self.lng, metoffer.DAILY)
        self.assertIsNotNone(forecast)

    def test_get_observation_data(self):
        met_office = MockMetOffice("ABCDEFGHIJKL",  observation=observation_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.get_observation_data(self.lat, self.lng)
        self.assertIsNotNone(forecast)

    def test_nearest_location_forecast_3hourly(self):
        met_office = MockMetOffice("ABCDEFGHIJKL", forecast=forecast_3hourly_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.nearest_location_forecast(self.lat, self.lng, metoffer.THREE_HOURLY)
        self.assertIsNotNone(forecast)

    def test_nearest_location_forecast_daily(self):
        met_office = MockMetOffice("ABCDEFGHIJKL", forecast=forecast_daily_payload)
        self.assertIsNotNone(met_office)
        forecast = met_office.nearest_location_forecast(self.lat, self.lng, metoffer.DAILY)
        self.assertIsNotNone(forecast)

    def test_observation(self):
        met_office = MockMetOffice("ABCDEFGHIJKL", observation=observation_payload)
        self.assertIsNotNone(met_office)

        observation = met_office.current_observation(self.lat, self.lng)
        self.assertIsNotNone(observation)

    def tes_five_day_forecast(self):
        met_office = MockMetOffice("ABCDEFGHIJKL", forecast=forecast_3hourly_payload)
        self.assertIsNotNone(met_office)

        forecast = met_office.five_day_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)

    def tets_twentyfour_hour_forecast(self):
        met_office = MockMetOffice("ABCDEFGHIJKL", forecast=forecast_daily_payload)
        self.assertIsNotNone(met_office)

        forecast = met_office.twentyfour_hour_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)


