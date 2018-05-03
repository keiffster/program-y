import unittest
import os

from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.security.authorise.authorisor import AuthorisationException

class BasicUserGroupAuthorisationServiceTests(unittest.TestCase):

    def test_usersgroups(self):
        service_config = BrainSecurityAuthorisationConfiguration("authorisation")
        service_config._usergroups = os.path.dirname(__file__) + os.sep + "test_usergroups.yaml"

        service = BasicUserGroupAuthorisationService(service_config)
        self.assertIsNotNone(service)

        self.assertTrue(service.authorise("console", "root"))
        self.assertFalse(service.authorise("console", "uber"))

        with self.assertRaises(AuthorisationException):
            service.authorise("anyone", "root")