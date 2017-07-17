import unittest

from programy.utils.security.authenticate.passthrough import BasicPassThroughAuthenticationService
from programy.config.sections.brain.service import BrainServiceConfiguration


class BasicPassThroughAuthenticationServiceTests(unittest.TestCase):

    def test_service(self):
        service = BasicPassThroughAuthenticationService(BrainServiceConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        self.assertTrue(service.authenticate("console"))
        self.assertTrue(service.authenticate("anyone"))
