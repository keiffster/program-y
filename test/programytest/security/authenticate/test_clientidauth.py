import unittest

from programy.security.authenticate.clientidauth import ClientIdAuthenticationService
from programy.config.sections.brain.security import BrainSecurityConfiguration

class MockClientIdAuthenticationService(ClientIdAuthenticationService):

    def __init__(self, brain_config):
        ClientIdAuthenticationService.__init__(self, brain_config)
        self.should_authorised = False
        self.raise_exception = False

    def user_auth_service(self, clientid):
        if self.raise_exception is True:
            raise Exception("Bad thing happen!")
        return self.should_authorised

class ClientIdAuthenticationServiceTests(unittest.TestCase):

    def test_init(self):
        service = ClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertTrue(service.authenticate("console"))
        self.assertFalse(service.authenticate("anyone"))

    def test_authorise_success(self):
        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = True
        self.assertTrue("console" in service.authorised)
        self.assertTrue(service.authenticate("console"))
        self.assertFalse("unknown" in service.authorised)
        self.assertTrue(service.authenticate("unknown"))
        self.assertTrue("unknown" in service.authorised)

    def test_authorise_failure(self):
        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = False
        self.assertFalse("unknown" in service.authorised)
        self.assertFalse(service.authenticate("unknown"))

    def test_authorise_exception(self):
        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = True
        service.raise_exception = True
        self.assertFalse(service.authenticate("unknown"))
