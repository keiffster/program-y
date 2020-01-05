import unittest

from programy.config.brain.service import BrainServiceConfiguration
from programy.security.authorise.passthrough import PassThroughAuthorisationService


class PassThroughAuthorisationServiceTests(unittest.TestCase):

    def test_authorisor(self):
        service = PassThroughAuthorisationService(BrainServiceConfiguration("authorisation"))
        self.assertIsNotNone(service)
        self.assertTrue(service.authorise("console", "sysadmin"))
        self.assertTrue(service.authorise("anyone", "sysadmin"))