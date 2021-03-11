import unittest
from unittest.mock import patch
from unittest.mock import Mock
from programy.services.base import Service
from programy.services.base import ServiceException
from programy.services.config import ServiceConfiguration
from programytest.client import TestClient


class ServiceExceptionTests(unittest.TestCase):

    def test_init(self):
        exception = ServiceException("Service failed")
        self.assertIsNotNone(exception)
        self.assertEquals('Service failed', str(exception))


class ServiceTests(unittest.TestCase):

    def test_init_empty_config(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")
        service = Service(config)
        self.assertIsNotNone(service)
        self.assertEqual(service.configuration, config)
        self.assertEquals([], service.patterns())
        self.assertIsNone(service.get_default_aiml_file())

    def test_init_defined_config(self):
        config = ServiceConfiguration.from_data("generic", "test", "category",
                                                service_class="testclass",
                                                default_response="default response",
                                                default_srai="default srai",
                                                storage="file",
                                                default_aiml="default.aiml")
        service = Service(config)
        self.assertIsNotNone(service)
        self.assertEqual(service.configuration, config)
        self.assertEqual("test", service.name)
        self.assertEqual("category", service.category)
        self.assertEquals([], service.patterns())
        client = TestClient()
        self.assertIsNone(service.get_default_aiml_file())

    def patch_ask_question(self, client_context, sentence):
        return "Default srai response"

    @patch("programy.bot.Bot.ask_question", patch_ask_question)
    def test_get_default_response_default_srai(self):
        config = ServiceConfiguration.from_data("generic", "test", "category", default_srai="TEST SERVICE FAILURE")
        service = Service(config)
        client = TestClient()
        client_context = client.create_client_context("testuser")
        self.assertEqual("Default srai response", service._get_default_response(client_context))

    def test_get_default_response_default_response(self):
        config = ServiceConfiguration.from_data("generic", "test", "category", default_response="This is the default response")
        service = Service(config)
        client = TestClient()
        client_context = client.create_client_context("testuser")
        self.assertEqual("This is the default response", service._get_default_response(client_context))

    def test_get_default_response_nothing(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")
        service = Service(config)
        client = TestClient()
        client_context = client.create_client_context("testuser")
        self.assertEqual("Service failed to return valid response", service._get_default_response(client_context))

    def test_load_default_aiml_by_config(self):
        config = ServiceConfiguration.from_data("generic", "test", "category",
                                                default_aiml="default.aiml")
        service = Service(config)
        self.assertIsNotNone(service)

        mock_aiml_parser = Mock()
        mock_aiml_parser.parse_from_file.return_value = True
        self.assertTrue(service.load_default_aiml(mock_aiml_parser))

    def patch_get_default_aiml_file(self):
        return "default.aiml"

    @patch("programy.services.base.Service.get_default_aiml_file", patch_get_default_aiml_file)
    def test_load_default_aiml_by_class(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")
        service = Service(config)
        self.assertIsNotNone(service)

        mock_aiml_parser = Mock()
        mock_aiml_parser.parse_from_file.return_value = True
        self.assertTrue(service.load_default_aiml(mock_aiml_parser))

    def test_load_default_aiml_nothing(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")
        service = Service(config)
        self.assertIsNotNone(service)

        mock_aiml_parser = Mock()
        mock_aiml_parser.parse_from_file.return_value = True
        self.assertFalse(service.load_default_aiml(mock_aiml_parser))

    def test_match(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")

        class MockQuery:

            @staticmethod
            def create(service):
                return MockQuery(service)

            def __init__(self, service):
                self._service = service

            def parse_matched(self, matched):
                pass

            def execute(self):
                return {'response': {'payload': 'Hi there', 'status': 'success'}}

            def aiml_response(self, response):
                return "Hi there from aiml"

        class MockService(Service):
            def __init__(self, configuration):
                Service.__init__(self, configuration)

            def patterns(self) -> list:
                return [
                    [r"HELLO", MockQuery]
                    ]

        service = MockService(config)
        self.assertIsNotNone(service)

        self.assertIsNotNone(service._match("HELLO"))

    def test_match_no_match(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")

        class MockQuery:

            @staticmethod
            def create(service):
                return MockQuery(service)

            def __init__(self, service):
                self._service = service

            def parse_matched(self, matched):
                pass

            def execute(self):
                return {'response': {'payload': 'Hi there', 'status': 'success'}}

            def aiml_response(self, response):
                return "Hi there from aiml"

        class MockService(Service):
            def __init__(self, configuration):
                Service.__init__(self, configuration)

            def patterns(self) -> list:
                return [
                    [r"HELLO", MockQuery]
                ]

        service = MockService(config)
        self.assertIsNotNone(service)

        self.assertIsNone(service._match("XXXX"))

    def test_execute_query(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")

        class MockQuery:

            @staticmethod
            def create(service):
                return MockQuery(service)

            def __init__(self, service):
                self._service = service

            def parse_matched(self, matched):
                pass

            def execute(self):
                return {'response': {'payload': 'Hi there', 'status': 'success'}}

            def aiml_response(self, response):
                return "Hi there from aiml"

        class MockService(Service):
            def __init__(self, configuration):
                Service.__init__(self, configuration)

            def patterns(self) -> list:
                return [
                    [r"HELLO", MockQuery]
                    ]

        mock_service = MockService(config)
        self.assertIsNotNone(mock_service)

        self.assertEqual({'response': {'payload': 'Hi there', 'status': 'success'}}, mock_service.execute_query("HELLO", aiml=False))
        self.assertEqual("Hi there from aiml", mock_service.execute_query("HELLO", aiml=True))

    def test_ask_question_with_response(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")

        class MockService(Service):
            def __init__(self, configuration):
                Service.__init__(self, configuration)

            def execute_query(self, question, aiml=False):
                return "Aiml response"

        service = MockService(config)
        self.assertIsNotNone(service)

        client = TestClient()
        client_context = client.create_client_context("testuser")

        self.assertEqual("Aiml response", service.ask_question(client_context, "Hello"))

    def test_ask_question_with_no_response(self):
        config = ServiceConfiguration.from_data("generic", "test", "category")

        class MockService(Service):
            def __init__(self, configuration):
                Service.__init__(self, configuration)

            def execute_query(self, question, aiml=False):
                return None

        service = MockService(config)
        self.assertIsNotNone(service)

        client = TestClient()
        client_context = client.create_client_context("testuser")

        self.assertEqual("Service failed to return valid response", service.ask_question(client_context, "Hello"))
