import datetime
import unittest
from programy.services.library.metoffice.metoffice import MetOffice5DayForecast
from programytest.services.library.metoffice.payloads.forecast_daily import forecast_daily_payload


class MockMetOffice5DayForecast(MetOffice5DayForecast):

    def __init__(self):
        MetOffice5DayForecast.__init__(self)

    def _calc_date_n_days_ahead(self, days, fromdate=None):
        time_then = datetime.datetime.strptime("2017-04-03Z", "%Y-%m-%dZ")
        return time_then + datetime.timedelta(days=days)


class MetOffice5DayForecastTests(unittest.TestCase):

    def test_parse_json(self):
        forecast = MockMetOffice5DayForecast()
        self.assertIsNotNone(forecast)

        forecast.parse_json(forecast_daily_payload)

        self.assertEquals(10, len(forecast.get_forecasts()))

        latest = forecast.get_latest_forecast()
        self.assertIsNotNone(latest)

        days = forecast.get_forecast_for_n_days_ahead(1)
        self.assertIsNotNone(days)
