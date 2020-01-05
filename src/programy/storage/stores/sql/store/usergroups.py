"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import os
import yaml
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.usergroups import UserGroupsStore
from programy.storage.stores.sql.dao.usergroup import AuthoriseUser
from programy.storage.stores.sql.dao.usergroup import UserRole
from programy.storage.stores.sql.dao.usergroup import UserGroup
from programy.storage.stores.sql.dao.usergroup import AuthoriseGroup
from programy.storage.stores.sql.dao.usergroup import GroupUser
from programy.storage.stores.sql.dao.usergroup import GroupGroup
from programy.storage.stores.sql.dao.usergroup import GroupRole
from programy.security.authorise.usergroups import User
from programy.security.authorise.usergroups import Group
from programy.storage.entities.store import Store
from programy.utils.console.console import outputLog


class SQLUserGroupStore(SQLStore, UserGroupsStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        UserGroupsStore.__init__(self)

    def _get_all(self):
        raise Exception("SQL User groups uses complex multi table data structure, do not call _get_all()")

    def empty(self):
        self._storage_engine.session.query(AuthoriseUser).delete()
        self._storage_engine.session.query(UserRole).delete()
        self._storage_engine.session.query(UserGroup).delete()
        self._storage_engine.session.query(AuthoriseGroup).delete()
        self._storage_engine.session.query(GroupUser).delete()
        self._storage_engine.session.query(GroupRole).delete()

    def load_from_yaml(self, yaml_data, verbose=False):
        self._upload_users(yaml_data, verbose)
        self._upload_groups(yaml_data, verbose)

    def _read_yaml_from_file(self, filename):
        with open(filename, 'r+') as yml_data_file:
            yaml_data = yaml.load(yml_data_file, Loader=yaml.FullLoader)
            self.load_from_yaml(yaml_data)

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):

        try:
            self._read_yaml_from_file(filename)
            self.commit(commit)
            return 1, 1

        except Exception as error:
            YLogger.exception(self, "Failed to load yaml file from [%s]", error, filename)

        return 0, 0

    def _upload_users(self, yaml_data, verbose=False):
        if 'users' in yaml_data:
            for user_name in yaml_data['users'].keys():

                auth_user = AuthoriseUser(name=user_name)
                result = self.storage_engine.session.add(auth_user)

                yaml_obj = yaml_data['users'][user_name]
                if 'roles' in yaml_obj:
                    roles_list = yaml_obj['roles']
                    splits = roles_list.split(",")
                    for role_name in splits:
                        role_name = role_name.strip()
                        user_role = UserRole(user=user_name, role=role_name)
                        if verbose is True:
                            outputLog(self, user_role)
                        self.storage_engine.session.add(user_role)

                if 'groups' in yaml_obj:
                    groups_list = yaml_obj['groups']
                    splits = groups_list.split(",")
                    for group_name in splits:
                        group_name = group_name.strip()
                        user_group = UserGroup(user=user_name, group=group_name)
                        if verbose is True:
                            outputLog(self, user_group)
                        self.storage_engine.session.add(user_group)

    def _upload_groups(self, yaml_data, verbose=False):
        if 'groups' in yaml_data:
            for group_name in yaml_data['groups'].keys():

                auth_group = AuthoriseGroup(name=group_name, parent=None)
                result = self.storage_engine.session.add(auth_group)

                yaml_obj = yaml_data['groups'][group_name]
                if 'roles' in yaml_obj:
                    roles_list = yaml_obj['roles']
                    splits = roles_list.split(",")
                    for role_name in splits:
                        role_name = role_name.strip()
                        group_role = GroupRole(group=group_name, role=role_name)
                        if verbose is True:
                            outputLog(self, group_role)
                        self.storage_engine.session.add(group_role)

                if 'groups' in yaml_obj:
                    groups_list = yaml_obj['groups']
                    splits = groups_list.split(",")
                    for element in splits:
                        inner_group_name = element.strip()
                        group_group = GroupGroup(group=group_name, subgroup=inner_group_name)
                        if verbose is True:
                            outputLog(self, group_group)
                        self.storage_engine.session.add(group_group)

                if 'users' in yaml_obj:
                    users_list = yaml_obj['users']
                    splits = users_list.split(",")
                    for user_name in splits:
                        user_name = user_name.strip()
                        group_user = GroupUser(group=group_name, user=user_name)
                        if verbose is True:
                            outputLog(self, group_user)
                        self.storage_engine.session.add(group_user)

    def load_usergroups(self, usersgroupsauthorisor):

        dbusers = self._storage_engine.session.query(AuthoriseUser)
        for dbuser in dbusers:
            user = User(dbuser.name)
            dbuserroles = self._storage_engine.session.query(UserRole).filter(UserRole.user == dbuser.name)
            for dbuserrole in dbuserroles:
                user.add_role(dbuserrole.role)
            dbusergroups = self._storage_engine.session.query(UserGroup).filter(UserGroup.user == dbuser.name)
            for dbusergroup in dbusergroups:
                user.add_group(dbusergroup.group)
            usersgroupsauthorisor.users[user.userid] = user

        groups = self._storage_engine.session.query(AuthoriseGroup)
        for dbgroup in groups:
            group = Group(dbgroup.name)
            groupusers = self._storage_engine.session.query(GroupUser).filter(GroupUser.group == dbgroup.name)
            for dbgroupuser in groupusers:
                group.add_user(dbgroupuser.user)
            groupgroups = self._storage_engine.session.query(GroupGroup).filter(GroupGroup.group == dbgroup.name)
            for dbgroupgroup in groupgroups:
                group.add_group(dbgroupgroup.subgroup)
            grouproles = self._storage_engine.session.query(GroupRole).filter(GroupRole.group == dbgroup.name)
            for dbgrouprole in grouproles:
                group.add_role(dbgrouprole.role)
            usersgroupsauthorisor.groups[group.groupid] = group

        self._combine_users_and_groups(usersgroupsauthorisor)
