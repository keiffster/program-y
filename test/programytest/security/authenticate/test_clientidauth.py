import unittest

from programy.security.authenticate.clientidauth import ClientIdAuthenticationService
from programy.config.sections.brain.security import BrainSecurityConfiguration
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.bot.bot import BotConfiguration
from programy.config.sections.brain.brain import BrainConfiguration

class MockClientIdAuthenticationService(ClientIdAuthenticationService):

    def __init__(self, brain_config):
        ClientIdAuthenticationService.__init__(self, brain_config)
        self.should_authorised = False
        self.raise_exception = False

    def user_auth_service(self, bot, clientid):
        if self.raise_exception is True:
            raise Exception("Bad thing happen!")
        return self.should_authorised

class ClientIdAuthenticationServiceTests(unittest.TestCase):

    def test_init(self):
        testbot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        service = ClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertTrue(service.authenticate(testbot, "console"))
        self.assertFalse(service.authenticate(testbot, "anyone"))

    def test_authorise_success(self):
        testbot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = True
        self.assertTrue("console" in service.authorised)
        self.assertTrue(service.authenticate(testbot, "console"))
        self.assertFalse("unknown" in service.authorised)
        self.assertTrue(service.authenticate(testbot, "unknown"))
        self.assertTrue("unknown" in service.authorised)

    def test_authorise_failure(self):
        testbot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = False
        self.assertFalse("unknown" in service.authorised)
        self.assertFalse(service.authenticate(testbot, "unknown"))

    def test_authorise_exception(self):
        testbot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = True
        service.raise_exception = True
        self.assertFalse(service.authenticate(testbot, "unknown"))
