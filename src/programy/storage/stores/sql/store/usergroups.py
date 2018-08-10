"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.usergroups import UserGroupsStore
from programy.storage.stores.sql.dao.usergroup import AuthoriseUser, UserRole, UserGroup, AuthoriseGroup, GroupUser, GroupRole
from programy.security.authorise.usergroups import User
from programy.security.authorise.usergroups import Group


class SQLUserGroupStore(SQLStore, UserGroupsStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def load_usergroups(self, usersgroupsauthorisor):

        dbusers = self._storage_engine.session.query(AuthoriseUser)
        for dbuser in dbusers:
            user = User(dbuser.userid)
            dbuserroles = self._storage_engine.session.query(UserRole).filter(UserRole.user==dbuser.userid)
            for dbuserrole in dbuserroles:
                user.add_role(dbuserrole.role)
            dbusergroups = self._storage_engine.session.query(UserGroup).filter(UserGroup.user==dbuser.userid)
            for dbusergroup in dbusergroups:
                user.add_group(dbusergroup.group)

        groups = self._storage_engine.session.query(AuthoriseGroup)
        for group in groups:
            groupusers = self._storage_engine.session.query(GroupUser).filter(GroupUser.group==group.name)
            grouprole = self._storage_engine.session.query(GroupRole).filter(GroupRole.group==group.name)

    def combine_users_and_groups(self, usergroups):

        for user_id in usergroups.users.keys():
            user = usergroups.users[user_id]

            new_groups = []
            for group_id in user.groups:
                if group_id in usergroups.groups:
                    group = usergroups.groups[group_id]
                    new_groups.append(group)
                else:
                    YLogger.error(self, "Unknown group id [%s] in user [%s]", group_id, user_id)
            user.add_groups(new_groups[:])

        for group_id in usergroups.groups.keys():
            group = usergroups.groups[group_id]

            new_groups = []
            for sub_group_id in group.groups:
                if sub_group_id in usergroups.groups:
                    new_group = usergroups.groups[sub_group_id]
                    new_groups.append(new_group)
                else:
                    YLogger.error(self, "Unknown group id [%s] in group [%s]", sub_group_id, group_id)
            group.add_groups(new_groups[:])

            new_users = []
            for sub_user_id in group.users:
                if sub_user_id in usergroups.users:
                    new_user = usergroups.users[sub_user_id]
                    new_users.append(new_user)
                else:
                    YLogger.error(self, "Unknown user id [%s] in group [%s]", sub_user_id, group_id)
            group.add_users(new_users[:])

    def get_storage(self):
        return self.storage_engine.configuration.usergroups_storage
