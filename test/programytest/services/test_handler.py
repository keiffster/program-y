import unittest
import os
from unittest.mock import Mock
from programy.services.handler import ServiceHandler
from programy.services.library.metoffice.service import MetOfficeService
from programy.services.library.wikipedia.service import WikipediaService
from programy.services.rest.accuweather.service import AccuWeatherService
from programy.services.rest.cocktaildb.service import CocktailDBService
from programy.services.rest.darksky.service import DarkSkyService
from programy.services.rest.duckduckgo.service import DuckDuckGoService
from programy.services.rest.geonames.service import GeoNamesService
from programy.services.rest.generic.service import GenericService
from programy.services.rest.getguidelines.service import GetGuidelinesService
from programy.services.rest.gnews.service import GNewsService
from programy.services.rest.goodreads.service import GoodReadsService
from programy.services.rest.google.geocode.service import GoogleGeoCodeService
from programy.services.rest.google.distance.service import GoogleDistanceService
from programy.services.rest.google.directions.service import GoogleDirectionsService
from programy.services.rest.newsapi.service import NewsAPIService
from programy.services.rest.omdb.service import OMDBService
from programy.services.rest.pandora.service import PandoraService
from programy.services.rest.programy.service import ProgramyService
from programy.services.rest.wolframalpha.service import WolframAlphaService
from programy.services.rest.worldtradingdata.service import WorldTradingDataStocksService
from programytest.client import TestClient
from programytest.externals import integration_tests_active, integration_tests_disabled


class ServiceHandlerTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(ServiceHandlerTestClient, self).load_storage()

        self.add_license_keys_store(filepath=os.path.dirname(__file__) + os.sep + "testdata" + os.sep + "license.keys")

        self.add_services_store(dirs=[MetOfficeService.get_default_conf_file(),
                                      WikipediaService.get_default_conf_file(),
                                      AccuWeatherService.get_default_conf_file(),
                                      CocktailDBService.get_default_conf_file(),
                                      DarkSkyService.get_default_conf_file(),
                                      DuckDuckGoService.get_default_conf_file(),
                                      GenericService.get_default_conf_file(),
                                      GeoNamesService.get_default_conf_file(),
                                      GetGuidelinesService.get_default_conf_file(),
                                      GNewsService.get_default_conf_file(),
                                      GoodReadsService.get_default_conf_file(),
                                      GoogleGeoCodeService.get_default_conf_file(),
                                      GoogleDistanceService.get_default_conf_file(),
                                      GoogleDirectionsService.get_default_conf_file(),
                                      NewsAPIService.get_default_conf_file(),
                                      OMDBService.get_default_conf_file(),
                                      PandoraService.get_default_conf_file(),
                                      ProgramyService.get_default_conf_file(),
                                      WolframAlphaService.get_default_conf_file(),
                                      WorldTradingDataStocksService.get_default_conf_file()
                                      ])
        self.add_pattern_nodes_store()
        self.add_template_nodes_store()

    def ask_question(self, userid, question):
        response = ""
        client_context = self.create_client_context(userid)
        try:
            self._questions += 1
            response = client_context.bot.ask_question(client_context, question, responselogger=self)

        except Exception as e:
            print("Error asking Test Client:", e)

        return response


class ServiceHandlerTests(unittest.TestCase):

    def test_init(self):
        handler = ServiceHandler()
        self.assertIsNotNone(handler)
        self.assertEqual({}, handler.services)

        mock_service = Mock()
        handler.add_service("test1", mock_service)

        self.assertTrue("test1" in handler.services)
        self.assertFalse("test2" in handler.services)

        handler.empty()

        self.assertFalse("test1" in handler.services)
        self.assertFalse("test2" in handler.services)

    @unittest.skipIf(integration_tests_active() is False, integration_tests_disabled)
    def test_load_services(self):
        client = ServiceHandlerTestClient()
        self.assertIsNotNone(client)

        client_context = client.create_client_context("test1")
        self.assertIsNotNone(client_context.brain._services)
        self.assertTrue("wikipedia" in client_context.brain._services.services)
        self.assertTrue("gnews" in client_context.brain._services.services)

        result = client.ask_question(client_context, "GNEWS SEARCH CHATBOTS")
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("<ul><li>"))