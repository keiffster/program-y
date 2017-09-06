import unittest

from programy.utils.security.authorise.passthrough import PassThroughAuthorisationService
from programy.config.sections.brain.service import BrainServiceConfiguration

class PassThroughAuthorisationServiceTests(unittest.TestCase):

    def test_authorisor(self):
        service = PassThroughAuthorisationService(BrainServiceConfiguration("authorisation"))
        self.assertIsNotNone(service)
        self.assertTrue(service.authorise("console", "sysadmin"))
        self.assertTrue(service.authorise("anyone", "sysadmin"))