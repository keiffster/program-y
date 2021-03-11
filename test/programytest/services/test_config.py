import unittest
from unittest.mock import Mock
import yaml
from programy.services.config import ServiceConfiguration
from programy.services.config import ServiceLibraryConfiguration
from programy.services.config import ServiceRESTConfiguration


class ServiceConfigurationTests(unittest.TestCase):

    def test_init(self):
        config = ServiceConfiguration(service_type='generic')
        self.assertIsNotNone(config)
        self.assertEqual(config.service_type, 'generic')
        self.assertIsNone(config.name)
        self.assertIsNone(config.category)
        self.assertIsNone(config.service_class)
        self.assertIsNone(config.storage)
        self.assertIsNone(config.default_aiml)
        self.assertIsNone(config.default_response)
        self.assertIsNone(config.default_srai)

    def test_from_yaml(self):
        yaml_data = yaml.load("""
        service:
            name: test
            category: test_category
            service_class: service.TestService
            default_response: Default Response
            default_srai: DEFAULT_SRAI
            default_aiml: test.aiml
        """, Loader=yaml.FullLoader)

        config = ServiceConfiguration.new_from_yaml(yaml_data, "test.yaml")
        self.assertIsNotNone(config)
        self.assertIsInstance(config, ServiceConfiguration)

        self.assertEqual(config.service_type, 'generic')

        self.assertEqual("test", config.name)
        self.assertEqual("test_category", config.category)

        self.assertEqual("test.yaml", config.storage)

        self.assertEqual("service.TestService", config.service_class)

        self.assertEqual(config.default_response, "Default Response")
        self.assertEqual(config.default_srai, "DEFAULT_SRAI")
        self.assertEqual(config.default_aiml, "test.aiml")

    def test_from_yaml_with_rest(self):
        yaml_data = yaml.load("""
        service:
            type: rest
            name: test
            category: test_category
            service_class: service.TestService
            default_response: Default Response
            default_srai: DEFAULT_SRAI
            default_aiml: test.aiml
            rest:
                retries: [10, 50, 100]
                timeout: 900
        """, Loader=yaml.FullLoader)

        config = ServiceConfiguration.new_from_yaml(yaml_data, "test.yaml")
        self.assertIsNotNone(config)
        self.assertIsInstance(config, ServiceRESTConfiguration)

        self.assertEqual("test", config.name)
        self.assertEqual("test_category", config.category)

        self.assertEqual("test.yaml", config.storage)

        self.assertEqual("service.TestService", config.service_class)

        self.assertEqual(config.default_response, "Default Response")
        self.assertEqual(config.default_srai, "DEFAULT_SRAI")
        self.assertEqual(config.default_aiml, "test.aiml")

        self.assertEqual(config.retries, [10, 50, 100])
        self.assertEqual(config.timeout, 900)

    def test_from_sql(self):
        mock_dao = Mock()
        mock_dao.name = "test"
        mock_dao.type = 'generic'
        mock_dao.category = "test_category"
        mock_dao.service_class = "service.TestService"
        mock_dao.default_response = "Default Response"
        mock_dao.default_srai = "DEFAULT_SRAI"
        mock_dao.default_aiml = "test.aiml"
        mock_dao.rest_retries = None
        mock_dao.rest_timeout = None

        config = ServiceConfiguration.from_sql(mock_dao)
        self.assertIsNotNone(config)
        self.assertIsInstance(config, ServiceConfiguration)

        self.assertEqual("test", config.name)
        self.assertEqual("test_category", config.category)

        self.assertEqual("sql", config.storage)

        self.assertEqual("service.TestService", config.service_class)

        self.assertEqual(config.default_response, "Default Response")
        self.assertEqual(config.default_srai, "DEFAULT_SRAI")
        self.assertEqual(config.default_aiml, "test.aiml")

    def test_from_sql_with_rest(self):
        mock_dao = Mock()
        mock_dao.type = 'rest'
        mock_dao.name = "test"
        mock_dao.category = "test_category"
        mock_dao.service_class = "service.TestService"
        mock_dao.default_response = "Default Response"
        mock_dao.default_srai = "DEFAULT_SRAI"
        mock_dao.default_aiml = "test.aiml"
        mock_dao.rest_retries = [10, 50, 100]
        mock_dao.rest_timeout = 900

        config = ServiceConfiguration.from_sql(mock_dao)
        self.assertIsNotNone(config)
        self.assertIsInstance(config, ServiceRESTConfiguration)

        self.assertEqual("test", config.name)
        self.assertEqual("test_category", config.category)

        self.assertEqual("sql", config.storage)

        self.assertEqual("service.TestService", config.service_class)

        self.assertEqual(config.default_response, "Default Response")
        self.assertEqual(config.default_srai, "DEFAULT_SRAI")
        self.assertEqual(config.default_aiml, "test.aiml")

    def test_from_mongo(self):
        service = {
            "type": 'library',
            "name": "test",
            "category": "test_category",
            "service_class": "service.TestService",
            "default_response": "Default Response",
            "default_srai": "DEFAULT_SRAI",
            "default_aiml": "test.aiml"
        }

        config = ServiceConfiguration.from_mongo(service)
        self.assertIsNotNone(config)
        self.assertIsInstance(config, ServiceLibraryConfiguration)

        self.assertEqual("test", config.name)
        self.assertEqual("test_category", config.category)

        self.assertEqual("mongo", config.storage)

        self.assertEqual("service.TestService", config.service_class)

        self.assertEqual(config.default_response, "Default Response")
        self.assertEqual(config.default_srai, "DEFAULT_SRAI")
        self.assertEqual(config.default_aiml, "test.aiml")

    def test_from_mongo_with_rest(self):
        service = {
            "type": 'rest',
            "name": "test",
            "category": "test_category",
            "service_class": "service.TestService",
            "default_response": "Default Response",
            "default_srai": "DEFAULT_SRAI",
            "default_aiml": "test.aiml",
            "rest": {
                "timeout": 900,
                "retries": [10, 50, 100]
            }
        }

        config = ServiceConfiguration.from_mongo(service)
        self.assertIsNotNone(config)
        self.assertIsInstance(config, ServiceRESTConfiguration)

        self.assertEqual("test", config.name)
        self.assertEqual("test_category", config.category)

        self.assertEqual("mongo", config.storage)

        self.assertEqual("service.TestService", config.service_class)

        self.assertEqual(config.default_response, "Default Response")
        self.assertEqual(config.default_srai, "DEFAULT_SRAI")
        self.assertEqual(config.default_aiml, "test.aiml")

        self.assertEqual(config.retries, [10, 50, 100])
        self.assertEqual(config.timeout, 900)
