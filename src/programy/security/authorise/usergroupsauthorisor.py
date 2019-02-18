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

from programy.utils.logging.ylogger import YLogger

from programy.security.authorise.authorisor import Authoriser
from programy.security.authorise.authorisor import AuthorisationException
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.storage.factory import StorageFactory

class BasicUserGroupAuthorisationService(Authoriser):

    def __init__(self, config: BrainSecurityAuthorisationConfiguration):
        Authoriser.__init__(self, config)
        self._users = {}
        self._groups = {}

    @property
    def users(self):
        return self._users

    @property
    def groups(self):
        return self._groups

    def initialise(self, client):
        self.load_users_and_groups(client)

    def load_users_and_groups(self, client):
        if client.storage_factory.entity_storage_engine_available(StorageFactory.USERGROUPS) is True:
            storage_engine = client.storage_factory.entity_storage_engine(StorageFactory.USERGROUPS)
            usergroups_store = storage_engine.usergroups_store()
            usergroups_store.load_usergroups(self)
        else:
            YLogger.warning(self, "No user groups defined, authorisation tag will not work!")

    def authorise(self, userid, role):
        if userid not in self._users:
            raise AuthorisationException("User [%s] unknown to system!"%userid)

        if userid in self._users:
            user = self._users[userid]
            return user.has_role(role)
        return False
