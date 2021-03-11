import unittest

from programy.storage.stores.sql.dao.service import Service


class ServiceTests(unittest.TestCase):

    def test_init(self):
        service1 = Service(type='rest', name='name', service_class='class')
        self.assertIsNotNone(service1)
        self.assertEqual(
            "<Service(id='n/a', type='rest', name='name', category='None', service_class='class', default_response='None', default_srai='None', default_aiml='None', load_default_aiml='True', success_prefix='None', url='None', rest_timeout='None', rest_retries='None')>",
            str(service1))

        service2 = Service(id=1, type='rest', name='name', service_class='class')
        self.assertIsNotNone(service2)
        self.assertEqual(
            "<Service(id='1', type='rest', name='name', category='None', service_class='class', default_response='None', default_srai='None', default_aiml='None', load_default_aiml='True', success_prefix='None', url='None', rest_timeout='None', rest_retries='None')>",
            str(service2))
