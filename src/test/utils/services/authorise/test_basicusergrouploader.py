import unittest

from programy.utils.services.authorise.basicusergrouploader import AuthorisationException
from programy.utils.services.authorise.basicusergrouploader import Authoriser
from programy.utils.services.authorise.basicusergrouploader import BasicUserGroupLoader

class UserGroupTests(unittest.TestCase):

    def test_loader(self):

        authoriser = BasicUserGroupLoader.load_users_and_groups()
        self.assertIsNotNone(authoriser)

        self.assertTrue(authoriser.authorise("console", "root"))

        self.assertFalse(authoriser.authorise("console", "roleX"))

        with self.assertRaises(AuthorisationException):
            authoriser.authorise("someone", "root")