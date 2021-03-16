import unittest
from unittest.mock import patch
import os
import metoffer
from programy.services.library.metoffice.service import MetOfficeService
from programy.services.config import ServiceConfiguration
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.services.library.metoffice.payloads.forecast_3hourly import forecast_3hourly_payload


class MetOfficeTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(MetOfficeTestClient, self).load_storage()
        self.add_license_keys_store(filepath=self.get_license_key_file())


class MetOffice24HourForecastServiceTests(ServiceTestCase):

    def test_init(self):
        service = MetOfficeService(ServiceConfiguration.from_data("library", "metoffice", "weather"))
        self.assertIsNotNone(service)
        client = MetOfficeTestClient()
        service.initialise(client)

    def patch_metoffer_24_hour_forecast_success(self, lat, lng):
        return forecast_3hourly_payload

    def _do_24_hour_forecast(self):
        service = MetOfficeService(ServiceConfiguration.from_data('rest', "metoffice", "weather"))

        self.assertIsNotNone(service)
        client = MetOfficeTestClient()
        service.initialise(client)

        response = service.forecast(56.0712, -3.1743, metoffer.THREE_HOURLY)
        payload = self.assertResponse(response, 'forecast', 'metoffice', 'weather')

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_24_hour_forecast_integration(self):
        self._do_24_hour_forecast()

    @patch("programy.services.library.metoffice.metoffice.MetOffice.twentyfour_hour_forecast", patch_metoffer_24_hour_forecast_success)
    def test_24_hour_forecast_unit(self):
        self._do_24_hour_forecast()

    def patch_get_current_date(self):
        return "2017-04-03Z"

    @patch("programy.services.library.metoffice.service.MetOfficeHoursForecastQuery._get_current_date", patch_get_current_date)
    @patch("programy.services.library.metoffice.metoffice.MetOffice.twentyfour_hour_forecast", patch_metoffer_24_hour_forecast_success)
    def test_handler_load_24_hour_forecast(self):
        client = MetOfficeTestClient()
        conf_file = MetOfficeService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "metoffice", "METOFFICE FORECAST LAT SIGN POS DEC 56 FRAC 0719912 LNG SIGN NEG DEC 3 FRAC 1750909 HOURS 3")
        self.assertIsNotNone(response)
        self.assertEqual("It will be a Sunny day , with a temperature of 4 'C.", response)

