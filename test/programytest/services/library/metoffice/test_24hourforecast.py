import datetime
import unittest
from programy.services.library.metoffice.metoffice import MetOffice24HourForecast
from programytest.services.library.metoffice.payloads.forecast_3hourly import forecast_3hourly_payload


class MockMetOffice24HourForecast(MetOffice24HourForecast):

        def __init__(self):
            MetOffice24HourForecast.__init__(self)

        def _calc_date_n_hours_ahead(self, hours, fromdate=None):
            time_then = datetime.datetime.strptime("2017-04-03Z", "%Y-%m-%dZ")
            return time_then + datetime.timedelta(hours=hours)


class MetOffice24HourForecastTests(unittest.TestCase):

    def test_parse_json(self):
        forecast =  MockMetOffice24HourForecast()
        self.assertIsNotNone(forecast)

        forecast.parse_json(forecast_3hourly_payload)

        hours = forecast.get_forecast_for_n_hours_ahead(0)
        self.assertIsNotNone(hours)

