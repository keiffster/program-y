"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


class Authorisable(object):

    def __init__(self, identifier):
        self._id = identifier
        self._roles = []
        self._groups = []

    @property
    def roles(self):
        return self._roles

    def add_role(self, role):
        if role not in self._roles:
            self.roles.append(role)

    def has_role(self, role):
        if role in self._roles:
            return True
        for group in self._groups:
            if group.has_role(role) is True:
                return True
        return False

    @property
    def groups(self):
        return self._groups

    def add_groups(self, groups):
        self._groups = groups[:]

    def add_group(self, group):
        if group not in self._groups:
            self._groups.append(group)

    def has_group(self, groupid):
        for group in self._groups:
            if groupid == group.groupid:
                return True
            elif group.has_group(groupid):
                return True
        return False

    def available_roles(self):
        roles = self._roles[:]
        for group in self._groups:
            roles += group.available_roles()
        return roles


class Group(Authorisable):

    def __init__(self, groupid):
        Authorisable.__init__(self, groupid)
        self._users = []

    @property
    def groupid(self):
        return self._id

    @property
    def users(self):
        return self._users

    def add_users(self, users):
        self._users = users[:]

    def add_user(self, user):
        if user not in self._users:
            self._users.append(user)

    def has_user(self, userid):
        for user in self._users:
            if user.userid == userid:
                return True
        return False


class User(Authorisable):

    def __init__(self, userid):
        Authorisable.__init__(self, userid)

    @property
    def userid(self):
        return self._id

    def add_to_group(self, group):
        if group not in self._groups:
            self._groups.append(group)
        group.add_user(self)
