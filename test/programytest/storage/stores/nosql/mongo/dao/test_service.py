import unittest

from programy.storage.stores.nosql.mongo.dao.service import Service


class ServiceTests(unittest.TestCase):

    def test_init_no_id(self):
        service = Service(name="test", service_class="test.serviceclass")

        self.assertIsNotNone(service)
        self.assertIsNone(service.id)
        self.assertEqual("test", service.name)
        self.assertEqual("test.serviceclass", service.service_class)
        self.assertEqual({'category': None,
                          'default_aiml': None,
                          'load_default_aiml': True,
                          'default_response': None,
                          'default_srai': None,
                          'success_prefix': None,
                          'name': 'test',
                          'rest_retries': None,
                          'rest_timeout': None,
                          'url': None,
                          'service_class': 'test.serviceclass',
                          'type': None}, service.to_document())

    def test_init_with_id(self):
        service = Service(name="test", service_class="test.serviceclass")
        service.id = '666'

        self.assertIsNotNone(service)
        self.assertIsNotNone(service.id)
        self.assertEqual('666', service.id)
        self.assertEqual("test", service.name)
        self.assertEqual("test.serviceclass", service.service_class)
        self.assertEqual({'_id': '666',
                          'category': None,
                          'default_aiml': None,
                          'load_default_aiml': True,
                          'default_response': None,
                          'default_srai': None,
                          'success_prefix': None,
                          'name': 'test',
                          'rest_retries': None,
                          'rest_timeout': None,
                          'url': None,
                          'service_class': 'test.serviceclass',
                          'type': None}, service.to_document())

    def test_from_document_no_id(self):
        service1 = Service.from_document({'name': 'test', 'service_class': 'test.serviceclass'})
        self.assertIsNotNone(service1)
        self.assertIsNone(service1.id)
        self.assertEqual("test", service1.name)
        self.assertEqual("test.serviceclass", service1.service_class)

    def test_from_document_with_id(self):
        service2 = Service.from_document({'_id': '666', 'name': 'test', 'service_class': 'test.serviceclass'})
        self.assertIsNotNone(service2)
        self.assertIsNotNone(service2.id)
        self.assertEqual('666', service2.id)
        self.assertEqual("test", service2.name)
        self.assertEqual("test.serviceclass", service2.service_class)

    def test_from_document_no_id(self):
        service1 = Service.from_document({'name': 'test', 'service_class': 'test.serviceclass'})
        self.assertEquals("<Service(id='n/a', type='None', name='test', category='None', service_class='None'default_response='None', default_srai='None', default_aiml='None', load_default_aiml='True', success_prefix='None', url='None')>", str(service1))

    def test_from_document_with_id(self):
        service2 = Service.from_document({'_id': '666', 'name': 'test', 'service_class': 'test.serviceclass'})
        self.assertEquals("<Service(id='666', type='None', name='test', category='None', service_class='None'default_response='None', default_srai='None', default_aiml='None', load_default_aiml='True', success_prefix='None', url='None')>", str(service2))

