import unittest
from unittest.mock import Mock
from unittest.mock import patch
from datetime import datetime
from datetime import timedelta
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceRESTConfiguration
from programytest.services.testcase import ServiceTestCase


class RESTExceptionServiceTests(ServiceTestCase):

    def test_init(self):
        exception = RESTServiceException("Service failed")
        self.assertIsNotNone(exception)
        self.assertEquals('Service failed', str(exception))


class RESTServiceTests(ServiceTestCase):

    def _create_service(self):
        class MockRESTService(RESTService):
            def __init__(self, configuration):
                RESTService.__init__(self, configuration)

            def _response_to_json(self, api, response):
                return response

        configuration = ServiceConfiguration.from_data("rest", "test", "category")
        return MockRESTService(configuration)

    def test_init(self):
        service = self._create_service()
        self.assertIsNotNone(service)

    def test_add_base_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        data = {"response": {}}
        started = datetime.now()
        speed = timedelta(microseconds=3000)
        service._add_base_payload(data, "success", "test", "http://some.service.com", "GET", 3, started, speed)

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "success")
        self.assertEqual(data['response']['url'], "http://some.service.com")
        self.assertEqual(data['response']['call'], "GET")
        self.assertEqual(data['response']['retries'], 3)
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

    def test_create_success_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        started = datetime.now()
        speed = timedelta(microseconds=3000)
        data = service._create_success_payload("test", "http://some.service.com", "GET", 3, started, speed, "response")

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "success")
        self.assertEqual(data['response']['url'], "http://some.service.com")
        self.assertEqual(data['response']['call'], "GET")
        self.assertEqual(data['response']['retries'], 3)
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

        self.assertTrue("payload" in data['response'])
        self.assertEqual("response", data['response']['payload'])

    def test_create_statuscode_failure_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        started = datetime.now()
        speed = timedelta(microseconds=3000)
        mock_response = Mock()
        mock_response.status_code = 500
        data = service._create_statuscode_failure_payload("test", "http://some.service.com", "GET", 3, started, speed, mock_response)

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "failure")
        self.assertEqual(data['response']['url'], "http://some.service.com")
        self.assertEqual(data['response']['call'], "GET")
        self.assertEqual(data['response']['retries'], 3)
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

        self.assertTrue("payload" in data['response'])
        self.assertEqual(data['response']['payload']['type'], 'statusCode')
        self.assertEqual(data['response']['payload']['statusCode'], 500)

    def test_create_http_failure_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        started = datetime.now()
        speed = timedelta(microseconds=3000)
        data = service._create_http_failure_payload("test", "http://some.service.com", "GET", 3, started, speed, "Service crashed")

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "failure")
        self.assertEqual(data['response']['url'], "http://some.service.com")
        self.assertEqual(data['response']['call'], "GET")
        self.assertEqual(data['response']['retries'], 3)
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

        self.assertTrue("payload" in data['response'])
        self.assertEqual(data['response']['payload']['type'], 'http')
        self.assertEqual(data['response']['payload']['httpError'], "Service crashed")

    def test_create_general_failure_payload(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        started = datetime.now()
        speed = timedelta(microseconds=3000)
        data = service._create_general_failure_payload("test", "http://some.service.com", "GET", 3, started, speed,
                                                       RESTServiceException("Something went wrong"))

        self.assertTrue('response' in data)
        self.assertEqual(data['response']['status'], "failure")
        self.assertEqual(data['response']['url'], "http://some.service.com")
        self.assertEqual(data['response']['call'], "GET")
        self.assertEqual(data['response']['retries'], 3)
        self.assertEqual(data['response']['started'], started.strftime("%d/%m/%Y, %H:%M:%S"))
        self.assertEqual(data['response']['speed'], "3.0ms")
        self.assertEqual(data['response']['service'], "test")
        self.assertEqual(data['response']['category'], "category")

        self.assertTrue("payload" in data['response'])
        self.assertEqual(data['response']['payload']['type'], 'general')
        self.assertEqual(data['response']['payload']['error'], "Something went wrong")

    def patch_requests_get(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = True
        return mock_response

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get)
    def test_do_get(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        response, count = service._do_get("http://some.api.com")
        self.assertEqual(0, count)
        self.assertIsNotNone(response)

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get)
    def test_get(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        response = service._get("test", "http://some.api.com")
        self.assertIsNotNone(response)
        self.assertTrue(response['response']['status'], 'success')

    def patch_requests_get_fail(self, url, headers, timeout):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.return_value = True
        return mock_response

    @patch("programy.services.rest.base.RESTService._requests_get", patch_requests_get_fail)
    def test_get_fail(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        response = service._get("test", "http://some.api.com")
        self.assertIsNotNone(response)
        self.assertTrue(response['response']['status'], 'failure')

    def patch_requests_post(self, url, headers, params, timeout):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = True
        return mock_response

    @patch("programy.services.rest.base.RESTService._requests_post", patch_requests_post)
    def test_do_post(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        response, count = service._do_post("http://some.api.com", {"query": "Hello"})
        self.assertEqual(0, count)
        self.assertIsNotNone(response)

    @patch("programy.services.rest.base.RESTService._requests_post", patch_requests_post)
    def test_post(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        response = service._post("test", "http://some.api.com", {"query": "Hello"})
        self.assertIsNotNone(response)
        self.assertTrue(response['response']['status'], 'success')

    def patch_requests_post_fail(self, url, headers, params, timeout):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.return_value = True
        return mock_response

    @patch("programy.services.rest.base.RESTService._requests_post", patch_requests_post_fail)
    def test_post_failure(self):
        service = self._create_service()
        self.assertIsNotNone(service)

        response = service._post("test", "http://some.api.com", {"query": "Hello"})
        self.assertIsNotNone(response)
        self.assertTrue(response['response']['status'], 'failure')


