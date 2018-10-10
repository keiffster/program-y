import unittest
import os

from programy.config.brain.security import BrainSecurityAuthorisationConfiguration

from programytest.client import TestClient

class AuthoriseTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(AuthoriseTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments):
        super(AuthoriseTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].security._authorisation = BrainSecurityAuthorisationConfiguration()
        self.configuration.client_configuration.configurations[0].configurations[0].security.authorisation._classname = "programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService"
        self.configuration.client_configuration.configurations[0].configurations[0].security.authorisation._denied_srai = "ACCESS_DENIED"
        self.configuration.client_configuration.configurations[0].configurations[0].security.authorisation._usergroups = os.path.dirname(__file__) + os.sep + "usergroups.yaml"


class AuthoriseAIMLTests(unittest.TestCase):

    def setUp(self):
        client = AuthoriseTestClient()
        self._client_context = client.create_client_context("console")

    def test_authorise_allowed(self):
        response = self._client_context.bot.ask_question(self._client_context, "ALLOW ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Access Allowed.')

    def test_authorise_denied(self):
        response = self._client_context.bot.ask_question(self._client_context, "DENY ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Sorry, but you are not authorised to access this content!')

    def test_authorise_denied_custom_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "CUSTOM DENY ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Sorry, but no chance!')
