import unittest

from programy.config.brain.securities import BrainSecuritiesConfiguration
from programy.config.brain.security import BrainSecurityAccountLinkerConfiguration
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.security.manager import SecurityManager
from programytest.client import TestClient


class MockSecurityManager(SecurityManager):

    def __init__(self, security_configuration, fail_authenticate=False, fail_authorise=False, fail_on_linked=False):
        SecurityManager.__init__(self, security_configuration)
        self._fail_authenticate = fail_authenticate
        self._fail_authorise = fail_authorise
        self._fail_on_linked = fail_on_linked

    def _load_authentication_class(self, client):
        if self._fail_authenticate is True:
            raise Exception("Mock exception")
        else:
            super(MockSecurityManager, self)._load_authentication_class(client)

    def _load_authorisation_class(self, client):
        if self._fail_authorise is True:
            raise Exception("Mock exception")
        else:
            super(MockSecurityManager, self)._load_authorisation_class(client)

    def _load_account_linking_class(self, client):
        if self._fail_on_linked is True:
            raise Exception("Mock exception")
        else:
            super(MockSecurityManager, self)._load_account_linking_class(client)


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

    def test_fail_load_authentication_class(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._account_linker = BrainSecurityAccountLinkerConfiguration()

        mgr = MockSecurityManager(config, fail_authenticate=True)
        self.assertIsNotNone(mgr)

        client = TestClient()
        mgr.load_security_services(client)

        self.assertIsNotNone(mgr.authorisation)
        self.assertIsNone(mgr.authentication)
        self.assertIsNotNone(mgr.account_linker)

    def test_fail_load_authentication_class_missing(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._authentication._classname = None
        config._account_linker = BrainSecurityAccountLinkerConfiguration()

        mgr = SecurityManager(config)
        self.assertIsNotNone(mgr)

        client = TestClient()
        mgr.load_security_services(client)

        self.assertIsNotNone(mgr.authorisation)
        self.assertIsNone(mgr.authentication)
        self.assertIsNotNone(mgr.account_linker)

    def test_fail_load_authorisation_class(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._account_linker = BrainSecurityAccountLinkerConfiguration()

        mgr = MockSecurityManager(config, fail_authorise=True)
        self.assertIsNotNone(mgr)

        client = TestClient()
        mgr.load_security_services(client)

        self.assertIsNone(mgr.authorisation)
        self.assertIsNotNone(mgr.authentication)
        self.assertIsNotNone(mgr.account_linker)

    def test_fail_load_authorisation_class_missing(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authorisation._classname = None
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._account_linker = BrainSecurityAccountLinkerConfiguration()

        mgr = SecurityManager(config)
        self.assertIsNotNone(mgr)

        client = TestClient()
        mgr.load_security_services(client)

        self.assertIsNone(mgr.authorisation)
        self.assertIsNotNone(mgr.authentication)
        self.assertIsNotNone(mgr.account_linker)

    def test_fail_load_account_linking_class(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._account_linker = BrainSecurityAccountLinkerConfiguration()

        mgr = MockSecurityManager(config, fail_on_linked=True)
        self.assertIsNotNone(mgr)

        client = TestClient()
        mgr.load_security_services(client)

        self.assertIsNotNone(mgr.authorisation)
        self.assertIsNotNone(mgr.authentication)
        self.assertIsNone(mgr.account_linker)

    def test_fail_load_account_linking_class_missing(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._account_linker = BrainSecurityAccountLinkerConfiguration()
        config._account_linker._classname = None

        mgr = SecurityManager(config)
        self.assertIsNotNone(mgr)

        client = TestClient()
        mgr.load_security_services(client)

        self.assertIsNotNone(mgr.authorisation)
        self.assertIsNotNone(mgr.authentication)
        self.assertIsNone(mgr.account_linker)
