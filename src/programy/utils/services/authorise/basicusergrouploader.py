"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.services.authorise.usergroups import User
from programy.utils.services.authorise.usergroups import Group


class AuthorisationException(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)


class Authoriser(object):

    def __init__(self, users, groups):
        self._users = users
        self._groups = groups

    def authorise(self, userid, role):
        if userid not in self._users:
            raise AuthorisationException("User [%s] unknown to system!")

        user = self._users[userid]
        return user.has_role(role)


class BasicUserGroupLoader(object):

    @classmethod
    def load_users_and_groups(cls):

        users = {}
        groups = {}

        console_user = User("console")
        users["console"] = console_user

        sysadmin_group = Group("sysadmin")
        groups["sysadmin"] = sysadmin_group

        sysadmin_group.add_role("root")

        console_user.add_to_group(sysadmin_group)

        return Authoriser(users, groups)

