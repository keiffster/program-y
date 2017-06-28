import unittest
import os

from programy.utils.services.service import Service, ServiceFactory
from programy.config.brain import BrainConfiguration, BrainServiceConfiguration

class MockService(Service):

    def __init__(self, config):
        Service.__init__(self, config)

    def ask_question(self, bot, clientid: str, question: str):
        return "asked"

class ServiceFactoryTests(unittest.TestCase):

    def test_load_services(self):

        service_config = BrainServiceConfiguration("mock", {'path': 'test.utils.services.test_service.MockService'})

        brain_config = BrainConfiguration()
        brain_config.services.append(service_config)

        ServiceFactory.preload_services(brain_config.services)

        self.assertIsNotNone(ServiceFactory.get_service("mock"))
        self.assertIsInstance(ServiceFactory.get_service("mock"), MockService)