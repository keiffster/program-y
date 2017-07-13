import unittest

from programy.utils.services.authentication import AuthenticationService
from programy.config.sections.brain.service import BrainServiceConfiguration

class PandoraServiceTests(unittest.TestCase):

    def test_ask_question(self):
        config = BrainServiceConfiguration("AUTHENTICATION")
        service = AuthenticationService(config)
        self.assertEqual("Hello", service.ask_question(None, "testid", "Hello"))