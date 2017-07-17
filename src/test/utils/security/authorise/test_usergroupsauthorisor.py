import unittest

from programy.utils.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.config.sections.brain.security import BrainSecurityConfiguration
from programy.utils.security.authorise.authorisor import AuthorisationException

class BasicUserGroupAuthorisationServiceTests(unittest.TestCase):

    def test_usersgroups(self):
        service = BasicUserGroupAuthorisationService(BrainSecurityConfiguration("authorisation"))
        self.assertIsNotNone(service)

        self.assertTrue(service.authorise("console", "root"))
        self.assertFalse(service.authorise("console", "uber"))

        with self.assertRaises(AuthorisationException):
            service.authorise("anyone", "root")