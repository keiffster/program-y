import unittest
import os

from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.security.authorise.authorisor import AuthorisationException
from programytest.client import TestClient

class BasicUserGroupAuthorisationServiceTests(unittest.TestCase):

    def test_usersgroups(self):
        client = TestClient()

        client.add_usergroups_store()

        service_config = BrainSecurityAuthorisationConfiguration("authorisation")
        service_config._usergroups = os.path.dirname(__file__) + os.sep + "test_usergroups.yaml"

        service = BasicUserGroupAuthorisationService(service_config)
        self.assertIsNotNone(service)

        service.initialise(client)

        self.assertTrue(service.authorise("console", "root"))
        self.assertFalse(service.authorise("console", "uber"))

        with self.assertRaises(AuthorisationException):
            service.authorise("anyone", "root")