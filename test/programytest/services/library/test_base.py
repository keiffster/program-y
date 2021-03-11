import unittest
from datetime import datetime
from datetime import timedelta
from programy.services.library.base import PythonAPIService
from programy.services.library.base import PythonAPIServiceException
from programy.services.config import ServiceConfiguration


class PythonAPIServiceExceptionTests(unittest.TestCase):

    def test_init(self):
        exception = PythonAPIServiceException("Service failed")
        self.assertIsNotNone(exception)
        self.assertEquals('Service failed', str(exception))


class PythonAPIServiceTests(unittest.TestCase):

    def _create_service(self):
        class MockPythonAPIService(PythonAPIService):
            def __init__(self, configuration):
                PythonAPIService.__init__(self, configuration)

            def _response_to_json(self, api, response):
                return response

        configuration = ServiceConfiguration.from_data("rest", "test", "category")
        return MockPythonAPIService(configuration)

    def test_init(self):
        service = self._create_service()
        self.assertIsNotNone(service)

    def test_add_base_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        data = {"response": {}}
        started = datetime.now()
        speed = timedelta(microseconds=3000)
        service._add_base_payload(data, "success", started, speed)

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "success")
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

    def test_create_success_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        started = datetime.now()
        speed = timedelta(microseconds=3000)
        data = service._create_success_payload("search", started, speed, "search results")

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "success")
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

        self.assertTrue('payload' in data['response'])
        self.assertEqual(data['response']['payload'], "search results")

    def test_create_failure_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        started = datetime.now()
        speed = timedelta(microseconds=3000)
        data = service._create_failure_payload("search", started, speed)

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "failure")
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

        self.assertTrue('payload' in data['response'])
        self.assertEqual(data['response']['payload']['type'], "general")

    def test_create_exception_failure_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        started = datetime.now()
        speed = timedelta(microseconds=3000)
        data = service._create_exception_failure_payload("search", started, speed, PythonAPIServiceException("Service failure"))

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "failure")
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

        self.assertTrue('payload' in data['response'])
        self.assertEqual(data['response']['payload']['type'], "general")
        self.assertEqual(data['response']['payload']['error'], "Service failure")
