import unittest
from unittest.mock import patch
from unittest.mock import Mock
import os
from programy.services.wsdl.nationalrailenquiries.service import NationalRailEnquiriesWSDLService
from programy.services.wsdl.nationalrailenquiries.service import NationalRailEnquiriesWSDLServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.wsdl.nationalrailenquiries.responses import get_arrival_boards_with_details_success


class NationalRailEnquiriesServiceTestClient(ServiceTestClient):

    def __init__(self):
        ServiceTestClient.__init__(self, debug=True)

    def load_storage(self):
        super(NationalRailEnquiriesServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class NationalRailEnquiriesWSDLServiceTests(ServiceTestCase):

    @unittest.skip("Broken wsdl")
    def test_init_with_wsdl(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._wsdl_file = os.path.dirname(__file__) + os.sep + 'nationalrailenquiries.wsdl'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

    def test_init_no_wsdl(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

    def test_init_no_wsdl_with_stationcodes(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        result = wsdl_client.get_station_name_from_code('KGH')
        self.assertEquals("KINGHORN",  result['response']['payload']['station_name'])

        result =  wsdl_client.get_station_code_from_name('KINGHORN')
        self.assertEquals("KGH", result['response']['payload']['station_code'])

        self.assertEquals([], wsdl_client._match_station("XXXXXXX"))


        self.assertEquals(['KINGHORN'], wsdl_client._match_station("Kinghorn"))

        self.assertEquals(['KIRKBY (MERSEYSIDE)', 'KIRKBY STEPHEN', 'KIRKBY-IN-ASHFIELD'], wsdl_client._match_station("Kirkby"))

    def test_get_arrival_boards_with_details(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_arrival_boards_with_details(10, 'KGH')

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('arrival_boards_with_details' in payload)

    def test_get_arrival_and_departure_boards_with_details(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_arrival_and_departure_boards_with_details(10, 'KGH')

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('arrival_and_departure_boards_with_details' in payload)

    def test_get_arrival_board(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_arrival_board(10, 'KGH')

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('arrival_board' in payload)

    def test_get_arrival_and_departure_boards(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_arrival_and_departure_boards(10, 'KGH')

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('arrival_and_departure_boards' in payload)

    def test_get_departure_board_with_details(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_departure_board_with_details(10, 'KGH')

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('departure_board_with_details' in payload)

    def test_get_departure_board(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_departure_board(10, 'KGH')

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('departure_board' in payload)

    def test_get_fastest_departures(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_fastest_departures('KGH', ['EDB'])

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('fastest_departures' in payload)

    def test_get_fastest_departures_with_details(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_fastest_departures_with_details('KGH', ['EDB'])

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('fastest_departures_with_details' in payload)

    def test_get_next_departures(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        details = wsdl_client.get_next_departures('KGH', ['EDB'])

        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('next_departures' in payload)

    def test_get_service_details(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        departures = wsdl_client.get_next_departures('KGH', ['EDB'])

        response = departures['response']
        payload = response['payload']
        next_departures = payload['next_departures']
        departures = next_departures['departures']
        destination = departures['destination'][0]
        service = destination['service']
        serviceID = service['serviceID']

        details = wsdl_client.get_service_details(serviceID)
        self.assertIsNotNone(details)
        self.assertTrue('response' in details)
        response = details['response']
        self.assertEquals(response['status'], 'success')
        self.assertTrue('payload' in response)
        payload = response['payload']
        self.assertTrue('service_details' in payload)

    def test_next_trains_from_station(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        response = wsdl_client.next_trains_from_station('Kinghorn')
        self.assertIsNotNone(response)

    def test_next_trains_from_station_platform(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        response = wsdl_client.next_trains_from_station(station='Kinghorn', platform='2')
        self.assertIsNotNone(response)

    def test_next_trains_from_station_platform_origin(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        response = wsdl_client.next_trains_from_station(station='Kinghorn', platform='2', origin="Edinburgh")
        self.assertIsNotNone(response)

    def test_next_trains_from_station_platform_destination(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        response = wsdl_client.next_trains_from_station(station='Kinghorn', destination="Edinburgh")
        self.assertIsNotNone(response)

    def test_next_trains_from_station_platform_origin_destination(self):

        config = NationalRailEnquiriesWSDLServiceConfiguration.from_data("wsdl", "nationalrailenquiries", "travel")
        config._station_codes_file = os.path.dirname(__file__) + os.sep + 'station_codes.csv'

        wsdl_client = NationalRailEnquiriesWSDLService(config)
        self.assertIsNotNone(wsdl_client)

        client = NationalRailEnquiriesServiceTestClient()
        wsdl_client.initialise(client)

        response = wsdl_client.next_trains_from_station(station='Kinghorn', platform='2', origin="Edinburgh", destination='Glenrothes with Thornton')

        self.assertIsNotNone(response)

    def test_handler_station_name(self):
        client = NationalRailEnquiriesServiceTestClient()
        conf_file = NationalRailEnquiriesWSDLService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "nationalrailenquiries", "NRE STATION NAME KGH")
        self.assertIsNotNone(response)
        self.assertEquals("NRE RESULT KINGHORN.", response)

    def test_next_train_from(self):
        client = NationalRailEnquiriesServiceTestClient()
        conf_file = NationalRailEnquiriesWSDLService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "nationalrailenquiries", "NRE NEXT TRAIN FROM KINGHORN PLATFORM 1")
        self.assertIsNotNone(response)
        self.assertRegex(response, "The next train from .* to .* is due at .*\.")

    def test_next_train_from_to(self):
        client = NationalRailEnquiriesServiceTestClient()
        conf_file = NationalRailEnquiriesWSDLService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "nationalrailenquiries", "NRE NEXT TRAIN FROM KINGHORN PLATFORM 1 TO EDINBURGH")
        self.assertIsNotNone(response)
        self.assertRegex(response, "The next train from .* to .* is due at .*\.")
