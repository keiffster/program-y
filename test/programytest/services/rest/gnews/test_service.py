import os
import unittest.mock
from unittest.mock import patch
from unittest.mock import Mock
from programy.services.rest.gnews.service import GNewsService
from programy.services.config import ServiceConfiguration
from programytest.services.testclient import ServiceTestClient
from programytest.services.testcase import ServiceTestCase
from programytest.externals import integration_tests_active, integration_tests_disabled
from programytest.services.rest.gnews.responses import search_success_response
from programytest.services.rest.gnews.responses import top_news_success_response
from programytest.services.rest.gnews.responses import topics_success_response
import logging


class GNewsServiceTestClient(ServiceTestClient):

    def __init__(self, debug=True):
        ServiceTestClient.__init__(self, debug=debug, level=logging.DEBUG)

    def load_storage(self):
        super(GNewsServiceTestClient, self).load_storage()
        self.add_license_keys_store(self.get_license_key_file())


class GNewsServiceTests(ServiceTestCase):

    def test_init(self):
        service = GNewsService(ServiceConfiguration.from_data("rest", "gnews", "news",))
        self.assertIsNotNone(service)

    def patch_requests_get_search_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = search_success_response
        return mock_response

    def patch_requests_get_top_news_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = top_news_success_response
        return mock_response

    def patch_requests_get_topics_success(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = topics_success_response
        return mock_response

    def do_search(self):
        service = GNewsService(ServiceConfiguration.from_data("rest", "gnews", "news"))
        client = GNewsServiceTestClient()
        service.initialise(client)
        self.assertIsNotNone(service)

        response = service.search("CHATBOTS")
        self.assertResponse(response, 'search', "gnews", "news")

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get_search_success)
    def test_search_unit(self):
        self.do_search()

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_search_integration(self):
        self.do_search()

    def do_top_news(self):
        service = GNewsService(ServiceConfiguration.from_data("rest", "gnews", "news"))
        client = GNewsServiceTestClient()
        service.initialise(client)
        self.assertIsNotNone(service)

        response = service.top_news()
        self.assertResponse(response, 'top_news', "gnews", "news")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_top_news_integration(self):
        self.do_top_news()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get_top_news_success)
    def test_top_news_unit(self):
        self.do_top_news()

    def do_topics(self):
        service = GNewsService(ServiceConfiguration.from_data("rest", "gnews", "news"))
        client = GNewsServiceTestClient()
        service.initialise(client)
        self.assertIsNotNone(service)

        response = service.topics("technology")
        self.assertResponse(response, 'topics', "gnews", "news")

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_topics_integration(self):
        self.do_topics()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get_topics_success)
    def test_topics_unit(self):
        self.do_topics()

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get_search_success)
    def test_search_aiml(self):
        client = GNewsServiceTestClient()
        conf_file = GNewsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "gnews", "GNEWS SEARCH CHATBOTS")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<ul><li>Recovering Lost Sales with Facebook Messenger Marketing</li>"))

    def test_topics_aiml(self):
        client = GNewsServiceTestClient()
        conf_file = GNewsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "gnews", "GNEWS TOPICS")
        self.assertIsNotNone(response)
        self.assertEqual(response, "<ul><li>world</li><li>nation</li><li>business</li><li>technology</li><li>entertainment</li><li>sports</li><li>science</li><li>health</li></ul>.")

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get_topics_success)
    def test_topic_aiml(self):
        client = GNewsServiceTestClient()
        conf_file = GNewsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "gnews", "GNEWS TOPIC TECHNOLOGY")
        self.assertIsNotNone(response)
        self.assertEqual(response, """<ul><li>A triple folding phone? Hands-on with TCL's working DragonHinge prototype</li>
<li>Windows 10 April 2020 Update</li>
<li>Miyamoto Says The Success Of The Switch Was All Thanks To The "Good Timing" Of Its Release</li>
<li>How to livestream the Oppo Find X2 and Oppo Smartwatch launch [Video]</li>
<li>Xbox Series X and PS5 graphics hardware will finally kiss goodbye to weird-looking hair</li>
<li>Santa Clara County Asks Apple, Google and Others to Cancel Large In-Person Meetings and Conferences</li>
<li>Porsche Explains Why The New 911 Turbo S Is Way More Powerful</li>
<li>Twitch Streamer Suspended After Accidentally Firing Real Gun At His Monitor</li>
<li>Pokemon Mystery Dungeon: Rescue Team DX Review</li>
<li>Apple Issues New Warning Affecting Millions Of iPhone Users</li></ul>.""")

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get_top_news_success)
    def test_topnews_aiml(self):
        client = GNewsServiceTestClient()
        conf_file = GNewsService.get_default_conf_file()

        response = self._do_handler_load(client, conf_file, "gnews", "GNEWS TOPNEWS EN UK")
        self.assertIsNotNone(response)
        self.assertEqual(response, "<ul><li>Coronavirus: Britons quarantined on cruise ship off San Francisco</li><li>Ceasefire in Syria after Russia and Turkey strike deal</li><li>Vatican City reports its first case of coronavirus, days after Pope tested negative</li><li>Bomb squad called and two held after suspicious device found in car in Luton</li><li>Boris Johnson's government has already spent £4.4bn on Brexit preparations, new figures reveal</li><li>Mum goes days without food in icy cold home and struggles sending son to £1 playgroup</li><li>Meghan Markle sends Twitter into meltdown as viewers think she ‘pushed’ Harry out the way</li><li>Supermarket rejects minister's food supplies claim</li><li>Coronavirus news</li><li>Amber Rudd hits out at 'rude' Oxford students after talk cancelled</li></ul>.")
