import unittest
import unittest.mock
from unittest.mock import patch
from programy.extensions.weather.weather import WeatherExtension
from programy.utils.geo.google import GoogleMaps
from programy.utils.weather.metoffice import MetOffice
from programytest.client import TestClient
from programytest.extensions.weather.payloads.google_latlong import latlong_payload
from programytest.extensions.weather.payloads.observation import observation_payload
from programytest.extensions.weather.payloads.forecast_3hourly import forecast_3hourly_payload
from programytest.extensions.weather.payloads.forecast_daily import forecast_daily_payload


class MockGoogleMaps(GoogleMaps):

    response = None

    def _get_response_as_json(self, url):
        return MockGoogleMaps.response


class MockMetOffice(MetOffice):

    response = None

    def _get_response_as_json(self):
        return MockMetOffice.response

    def get_forecast_data(self, lat, lon, forecast_type):
        return self._get_response_as_json()

    def get_observation_data(self, lat, lon):
        return self._get_response_as_json()


class MockWeatherExtension(WeatherExtension):

    def __init__(self, fromdate=None):
        self._fromdate = fromdate

    def get_geo_locator(self):
        return MockGoogleMaps()

    def get_met_office(self):
        return MockMetOffice()

    def get_from_date(self):
        return self._fromdate


class WeatherExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self.context = client.create_client_context("testid")

        bot = unittest.mock.Mock()
        self.context.bot = bot
        self.context.brain = bot.brain

    def test_get_geo_locator(self):
        weather = WeatherExtension()
        self.assertIsInstance(weather.get_geo_locator(), GoogleMaps)

    def test_get_met_office(self):
        weather = WeatherExtension()
        self.assertIsInstance(weather.get_met_office(), MetOffice)

    def test_weather_invalid(self):
        weather = WeatherExtension()
        self.assertIsNone(weather.execute(self.context, ""))
        self.assertIsNone(weather.execute(self.context, "OTHER"))

        self.assertIsNone(weather.execute(self.context, "OBSERVATION"))
        self.assertIsNone(weather.execute(self.context, "FORECAST5DAY"))
        self.assertIsNone(weather.execute(self.context, "FORECAST24HOUR"))

        self.assertIsNone(weather.execute(self.context, "OBSERVATION OTHER"))
        self.assertIsNone(weather.execute(self.context, "FORECAST5DAY OTHER"))
        self.assertIsNone(weather.execute(self.context, "FORECAST24HOUR OTHER"))

        self.assertIsNone(weather.execute(self.context, "OBSERVATION LOCATION"))
        self.assertIsNone(weather.execute(self.context, "FORECAST5DAY LOCATION"))
        self.assertIsNone(weather.execute(self.context, "FORECAST24HOUR LOCATION"))

        self.assertIsNone(weather.execute(self.context, "OBSERVATION LOCATION EDINBURGH"))
        self.assertIsNone(weather.execute(self.context, "FORECAST5DAY LOCATION EDINBURGH"))
        self.assertIsNone(weather.execute(self.context, "FORECAST24HOUR LOCATION EDINBURGH"))

        self.assertIsNone(weather.execute(self.context, "OBSERVATION LOCATION EDINBURGH WHEN"))
        self.assertIsNone(weather.execute(self.context, "FORECAST5DAY LOCATION EDINBURGH WHEN"))
        self.assertIsNone(weather.execute(self.context, "FORECAST24HOUR LOCATION EDINBURGH WHEN"))

        self.assertIsNone(weather.execute(self.context, "OTHER LOCATION EDINBURGH WHEN 1"))

        self.assertIsNone(weather.execute(self.context, "OBSERVATION OTHER EDINBURGH WHEN 1"))
        self.assertIsNone(weather.execute(self.context, "FORECAST5DAY OTHER EDINBURGH WHEN 1"))
        self.assertIsNone(weather.execute(self.context, "FORECAST24HOUR OTHER EDINBURGH WHEN 1"))

        self.assertIsNone(weather.execute(self.context, "OBSERVATION LOCATION EDINBURGH OTHER 1"))
        self.assertIsNone(weather.execute(self.context, "FORECAST5DAY LOCATION EDINBURGH OTHER 1"))
        self.assertIsNone(weather.execute(self.context, "FORECAST24HOUR LOCATION EDINBURGH OTHER 1"))

    def test_current_observation(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = observation_payload

        weather = MockWeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER Partly cloudy (day) TEMP 12 3 HUMIDITY 57 3 VISIBILITY V 35000 VF Very Good PRESSURE P 1017 PT F PTF Falling WIND D SW DF South West S 10", result)

        result = weather.execute(self.context, "OBSERVATION OTHER KY39UR WHEN NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR OTHER NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "")
        self.assertIsNone(result)

    def patch_current_observation(self, lat, lng):
        return None

    @patch("programy.utils.weather.metoffice.MetOffice.current_observation", patch_current_observation)
    def test_current_observation_when_observation_is_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_daily_payload

        weather = MockWeatherExtension()

        self.assertEquals("UNAVAILABLE", weather.execute(self.context, "OBSERVATION LOCATION KY39UR WHEN NOW"))

    def test_forecast24hour_from_date_is_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_3hourly_payload

        weather = MockWeatherExtension()
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST24HOUR LOCATION KY39UR WHEN 1")

        self.assertIsNotNone(result)
        self.assertEqual(
            "WEATHER Overcast TEMP 10 FEELS 10 WINDSPEED 4 UVINDEX 0 UVGUIDE None RAINPROB 8 HUMIDITY 73 WINDDIR NW WINDDIRFULL North West VIS Very good - Between 20-40 km",
            result)

    def test_forecast24hour_from_date_is_not_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_3hourly_payload

        weather = MockWeatherExtension("2017-04-03Z")
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST24HOUR LOCATION KY39UR WHEN 1")

        self.assertIsNotNone(result)
        self.assertEqual("WEATHER Sunny day TEMP 4 FEELS 3 WINDSPEED 2 UVINDEX 1 UVGUIDE Low exposure. No protection required. You can safely stay outside RAINPROB 0 HUMIDITY 96 WINDDIR S WINDDIRFULL South VIS Moderate - Between 4-10 km", result)

    def patch_twentyfour_hour_forecast(self, lat, lng):
        return None

    @patch("programy.utils.weather.metoffice.MetOffice.twentyfour_hour_forecast", patch_twentyfour_hour_forecast)
    def test_forecast24hour_when_twentyfour_hour_forecast_is_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_3hourly_payload

        weather = MockWeatherExtension()

        self.assertEquals("UNAVAILABLE", weather.execute(self.context, "FORECAST24HOUR LOCATION KY39UR WHEN 1"))

    def patch_to_program_y_text(self):
        return None

    @patch("programy.utils.weather.metoffice.ThreeHourlyForecastDataPoint.to_program_y_text", patch_to_program_y_text)
    def test_forecast24hour_when_to_program_y_text_is_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_3hourly_payload

        weather = MockWeatherExtension()

        self.assertEquals("UNAVAILABLE", weather.execute(self.context, "FORECAST24HOUR LOCATION KY39UR WHEN 1"))

    def test_forecast5day_fromdate_is_date(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_daily_payload

        weather = MockWeatherExtension("2017-04-03Z")

        result = weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER TYPE Day WINDDIR N WINDSPEED 7 WINDGUST 11 TEMP 13 FEELS 11 HUMID 82RAINPROB 49 UVINDEX 2 UVGUIDE Low exposure. No protection required. You can safely stay outside VIS Good - Between 10-20 km WEATHER Overcast", result)

    def test_forecast5day_fromdate_is_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_daily_payload

        weather = MockWeatherExtension()
        weather.fromdate = None

        result = weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1")
        self.assertIsNotNone(result)
        self.assertEqual("WEATHER TYPE Cloudy WINDDIR NW WINDGUST 7 WINDSPEED 4 TEMP 8 FEELS 8 HUMID 76 RAINPROB 8 VISTEXT Very good - Between 20-40 km WEATHER Cloudy", result)

    def patch_five_day_forecast(self, lat, lng):
        return None

    @patch("programy.utils.weather.metoffice.MetOffice.five_day_forecast", patch_five_day_forecast)
    def test_forecast5day_when_twentyfour_hour_forecast_is_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_daily_payload

        weather = MockWeatherExtension()

        self.assertEquals("UNAVAILABLE", weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1"))

    def patch_five_day_forecast2(self, lat, lng):
        raise Exception("Mock Exception")

    @patch("programy.utils.weather.metoffice.MetOffice.five_day_forecast", patch_five_day_forecast2)
    def test_forecast5day_when_twentyfour_hour_forecast_is_exception(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_daily_payload

        weather = MockWeatherExtension()

        self.assertEquals("UNAVAILABLE", weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1"))

    @patch("programy.utils.weather.metoffice.DailyForecastNightDataPoint.to_program_y_text", patch_to_program_y_text)
    def test_forecast5day_when_to_program_y_text_is_none(self):
        MockGoogleMaps.response = latlong_payload
        MockMetOffice.response = forecast_daily_payload

        weather = MockWeatherExtension()

        self.assertEquals("UNAVAILABLE", weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1"))

