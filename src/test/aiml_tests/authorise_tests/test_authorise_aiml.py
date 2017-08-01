import unittest
import os

from programy.config.sections.brain.security import BrainSecurityConfiguration

from test.aiml_tests.client import TestClient

class AuthoriseTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(AuthoriseTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)
        self.configuration.brain_configuration.security._authorisation = BrainSecurityConfiguration("authorisation")
        self.configuration.brain_configuration.security.authorisation._classname = "programy.utils.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService"
        self.configuration.brain_configuration.security.authorisation._denied_srai = "ACCESS_DENIED"
        self.configuration.brain_configuration.security.authorisation._usergroups = os.path.dirname(__file__) + os.sep + "usergroups.yaml"

class AuthoriseAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AuthoriseAIMLTests.test_client = AuthoriseTestClient()

    def test_authorise_allowed(self):
        response = AuthoriseAIMLTests.test_client.bot.ask_question("console", "ALLOW ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Access Allowed')

    def test_authorise_denied(self):
        response = AuthoriseAIMLTests.test_client.bot.ask_question("console", "DENY ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Sorry, but you are not authorised to access this content!')

    def test_authorise_denied_custom_response(self):
        response = AuthoriseAIMLTests.test_client.bot.ask_question("console", "CUSTOM DENY ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Sorry, but no chance!')
