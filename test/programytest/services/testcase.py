import unittest
import yaml
from programy.services.config import ServiceConfiguration


class ServiceTestCase(unittest.TestCase):

    def _load_conf_file(self, client_context, conf_file):
        with open(conf_file, 'r+', encoding="utf-8") as yml_data_file:
            yaml_data = yaml.load(yml_data_file, Loader=yaml.FullLoader)

            config = ServiceConfiguration.new_from_yaml(yaml_data, conf_file)

            client_context.brain.service_handler.load_service(config)

            client_context.brain.service_handler.post_initialise(client_context.brain)

    def _do_handler_load(self, client, conf_file, name, question):

        client_context = client.create_client_context("testuser")

        self._load_conf_file(client_context, conf_file)

        self.assertTrue(name in client_context.brain.service_handler.services)

        return client_context.bot.ask_question(client_context, question)

    def assertResponse(self, response, api, service, category):
        self.assertIsNotNone(response)

        self.assertTrue('response' in response)
        response = response['response']

        self.assertTrue('api' in response)
        self.assertEqual(api, response['api'])

        self.assertTrue('started' in response)
        self.assertTrue('speed' in response)
        self.assertTrue('status' in response)
        self.assertEqual('success', response['status'])
        self.assertTrue('service' in response)
        self.assertEqual(service, response['service'])
        self.assertTrue('category' in response)
        self.assertEqual(category, response['category'])
        self.assertTrue('payload' in response)

        return response['payload']
