import unittest

from programy.utils.services.authenticate.passthrough import PassThroughAuthenticationService
from programy.config.sections.brain.service import BrainServiceConfiguration

class PassThroughAuthenticationServiceTests(unittest.TestCase):

    def test_ask_question(self):
        config = BrainServiceConfiguration("AUTHENTICATION")
        service = PassThroughAuthenticationService(config)
        self.assertEqual("Hello", service.ask_question(None, "testid", "Hello"))