import unittest
import metoffer
from programy.services.library.metoffice.metoffice import DataPoint
from programy.services.library.metoffice.metoffice import MetOfficeWeatherReport


class DataPointTest(unittest.TestCase):

    def test_init(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

    def test_extract_attribute(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

        self.assertEqual("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.OBSERVATION))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.OBSERVATION, None))

        self.assertEqual("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY))

        self.assertEqual("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.FORECAST,metoffer.DAILY))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.FORECAST,metoffer.DAILY))

        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", 3))

    def test_direction_to_full_text(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

        self.assertEqual(dp.direction_to_full_text('N'), 'North')
        self.assertEqual(dp.direction_to_full_text('NNE'), 'North North East')
        self.assertEqual(dp.direction_to_full_text('NE'), 'North East')
        self.assertEqual(dp.direction_to_full_text('ENE'), 'East North East')
        self.assertEqual(dp.direction_to_full_text('E'), 'East')
        self.assertEqual(dp.direction_to_full_text('ESE'), 'East South East')
        self.assertEqual(dp.direction_to_full_text('SE'), 'South East')
        self.assertEqual(dp.direction_to_full_text('SSE'), 'South South East')
        self.assertEqual(dp.direction_to_full_text('S'), 'South')
        self.assertEqual(dp.direction_to_full_text('SSW'), 'South South West')
        self.assertEqual(dp.direction_to_full_text('SW'), 'South West')
        self.assertEqual(dp.direction_to_full_text('WSW'), 'West South West')
        self.assertEqual(dp.direction_to_full_text('W'), 'West')
        self.assertEqual(dp.direction_to_full_text('WNW'), 'West North West')
        self.assertEqual(dp.direction_to_full_text('NW'), 'North West')
        self.assertEqual(dp.direction_to_full_text('NNW'), 'North North West')

        self.assertEqual(dp.direction_to_full_text(''), "Unknown")
        self.assertEqual(dp.direction_to_full_text('other'), "Unknown")
        self.assertEqual(dp.direction_to_full_text(None), "Unknown")
