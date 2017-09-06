import unittest

from programy.utils.security.authenticate.authenticator import Authenticator
from programy.config.sections.brain.security import BrainSecurityConfiguration


class AuthenticatorTests(unittest.TestCase):

    def test_authenticator_with_empty_config(self):
        service = Authenticator(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        self.assertIsNone(service.get_default_denied_srai())
        self.assertFalse(service.authenticate("console"))
