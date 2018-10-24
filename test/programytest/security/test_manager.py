import unittest

from programy.security.manager import SecurityManager
from programy.config.brain.securities import BrainSecuritiesConfiguration
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.config.brain.security import BrainSecurityAccountLinkerConfiguration
from programytest.client import TestClient

class TestSecurityManager(unittest.TestCase):

    def test_init(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._account_linker = BrainSecurityAccountLinkerConfiguration()

        mgr = SecurityManager(config)
        self.assertIsNotNone(mgr)

        client = TestClient()

        mgr.load_security_services(client)

        self.assertIsNotNone(mgr.authorisation)
        self.assertIsNotNone(mgr.authentication)
        self.assertIsNotNone(mgr.account_linker)