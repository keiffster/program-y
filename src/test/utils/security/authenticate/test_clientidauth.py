import unittest

from programy.utils.security.authenticate.clientidauth import ClientIdAuthenticationService
from programy.config.sections.brain.security import BrainSecurityConfiguration


class ClientIdAuthenticationServiceTests(unittest.TestCase):

    def test_service(self):
        service = ClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertTrue(service.authenticate("console"))
        self.assertFalse(service.authenticate("anyone"))
