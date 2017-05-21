import unittest
import os

from programy.utils.weather.metoffice import MetOffice, DailyForecastDayDataPoint, DailyForecastNightDataPoint, ThreeHourlyForecastDataPoint, ObservationDataPoint
from programy.utils.text.dateformat import DateFormatter
from programy.utils.license.keys import LicenseKeys

class MetOfficeWeatherExtensionIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.license_keys = LicenseKeys()
        self.license_keys.load_license_key_file(os.path.dirname(__file__)+"/../../../../bots/y-bot/config/license.keys")

        self.lat = 56.0720397
        self.lng = -3.1752001

    def test_observation(self):
        met_office = MetOffice(self.license_keys)
        self.assertIsNotNone(met_office)

        observation = met_office.current_observation(self.lat, self.lng)
        self.assertIsNotNone(observation)

        report = observation.get_latest_report()
        self.assertIsNotNone(report)

        date = DateFormatter.year_month_day_now()
        report = observation.get_report_for_date(date)
        self.assertIsNotNone(report)

        datapoint = report.get_time_period_by_time("300")
        self.assertIsNotNone(datapoint)
        self.assertIsInstance(datapoint, ObservationDataPoint)

    def test_threehourly_forecast(self):
        met_office = MetOffice(self.license_keys)
        self.assertIsNotNone(met_office)

        forecast = met_office.three_hourly_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)

        report = forecast.get_latest_report()
        self.assertIsNotNone(report)

        date = DateFormatter.year_month_day_now()
        report = forecast.get_report_for_date(date)
        self.assertIsNotNone(report)

        datapoint = report.get_time_period_by_time("900")
        self.assertIsNotNone(datapoint)
        self.assertIsInstance(datapoint, ThreeHourlyForecastDataPoint)

    def test_daily_forecast(self):
        met_office = MetOffice(self.license_keys)
        self.assertIsNotNone(met_office)

        forecast = met_office.daily_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)

        report = forecast.get_latest_report()
        self.assertIsNotNone(report)

        date = DateFormatter.year_month_day_now()
        report = forecast.get_report_for_date(date)
        self.assertIsNotNone(report)

        day_datapoint = report.get_time_period_by_type('Day')
        self.assertIsNotNone(day_datapoint)
        self.assertIsInstance(day_datapoint, DailyForecastDayDataPoint)

        night_datapoint = report.get_time_period_by_type('Night')
        self.assertIsNotNone(night_datapoint)
        self.assertIsInstance(night_datapoint, DailyForecastNightDataPoint)
