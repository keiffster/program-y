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
import yaml
import os

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.usergroups import UserGroupsStore
from programy.storage.stores.sql.dao.usergroup import AuthoriseUser, UserRole, UserGroup, AuthoriseGroup, GroupUser, GroupGroup, GroupRole
from programy.security.authorise.usergroups import User, Group
from programy.storage.entities.store import Store

class SQLUserGroupStore(SQLStore, UserGroupsStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(AuthoriseUser).delete()
        self._storage_engine.session.query(UserRole).delete()
        self._storage_engine.session.query(UserGroup).delete()
        self._storage_engine.session.query(AuthoriseGroup).delete()
        self._storage_engine.session.query(GroupUser).delete()
        self._storage_engine.session.query(GroupRole).delete()

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):

        if os.path.exists(filename):
            try:
                with open(filename, 'r+') as yml_data_file:
                    yaml_data = yaml.load(yml_data_file, Loader=yaml.FullLoader)
                    self._upload_users(yaml_data, verbose)
                    self._upload_groups(yaml_data, verbose)

                if commit is True:
                    self.commit()

            except FileNotFoundError:
                YLogger.error(self, "File not found [%s]", filename)

            return 1,1
        return 0, 0

    def _upload_users(self, yaml_data, verbose=False):
        if 'users' in yaml_data:
            for user_name in yaml_data['users'].keys():

                auth_user = AuthoriseUser(name=user_name)
                self.storage_engine.session.add(auth_user)

                yaml_obj = yaml_data['users'][user_name]
                if 'roles' in yaml_obj:
                    roles_list = yaml_obj['roles']
                    splits = roles_list.split(",")
                    for role_name in splits:
                        role_name = role_name.strip()
                        user_role = UserRole(user=user_name, role=role_name)
                        if verbose is True:
                            print(user_role)
                        self.storage_engine.session.add(user_role)

                if 'groups' in yaml_obj:
                    groups_list = yaml_obj['groups']
                    splits = groups_list.split(",")
                    for group_name in splits:
                        group_name = group_name.strip()
                        user_group = UserGroup(user=user_name, group=group_name)
                        if verbose is True:
                            print(user_group)
                        self.storage_engine.session.add(user_group)

    def _upload_groups(self, yaml_data, verbose=False):
        if 'groups' in yaml_data:
            for group_name in yaml_data['groups'].keys():

                auth_group = AuthoriseGroup(name=group_name)
                self.storage_engine.session.add(auth_group)

                yaml_obj = yaml_data['groups'][group_name]
                if 'roles' in yaml_obj:
                    roles_list = yaml_obj['roles']
                    splits = roles_list.split(",")
                    for role_name in splits:
                        role_name = role_name.strip()
                        group_role = GroupRole(group=group_name, role=role_name)
                        if verbose is True:
                            print(group_role)
                        self.storage_engine.session.add(group_role)

                if 'groups' in yaml_obj:
                    groups_list = yaml_obj['groups']
                    splits = groups_list.split(",")
                    for element in splits:
                        inner_group_name = element.strip()
                        group_group = GroupGroup(group=group_name, subgroup=inner_group_name)
                        if verbose is True:
                            print(group_group)
                        self.storage_engine.session.add(group_group)

                if 'users' in yaml_obj:
                    users_list = yaml_obj['groups']
                    splits = users_list.split(",")
                    for user_name in splits:
                        user_name = user_name.strip()
                        group_user = GroupUser(group=group_name, user=user_name)
                        if verbose is True:
                            print(group_user)
                        self.storage_engine.session.add(group_user)

    def load_usergroups(self, usersgroupsauthorisor):

        dbusers = self._storage_engine.session.query(AuthoriseUser)
        for dbuser in dbusers:
            user = User(dbuser.name)
            dbuserroles = self._storage_engine.session.query(UserRole).filter(UserRole.user==dbuser.name)
            for dbuserrole in dbuserroles:
                user.add_role(dbuserrole.role)
            dbusergroups = self._storage_engine.session.query(UserGroup).filter(UserGroup.user==dbuser.name)
            for dbusergroup in dbusergroups:
                user.add_group(dbusergroup.group)
            usersgroupsauthorisor.users[user.userid]=user

        groups = self._storage_engine.session.query(AuthoriseGroup)
        for dbgroup in groups:
            group = Group(dbgroup.name)
            groupusers = self._storage_engine.session.query(GroupUser).filter(GroupUser.group==dbgroup.name)
            for dbgroupuser in groupusers:
                group.add_user(dbgroupuser.name)
            groupgroups = self._storage_engine.session.query(GroupGroup).filter(GroupGroup.group==dbgroup.name)
            for dbgroupgroup in groupgroups:
                group.add_group(dbgroupgroup.subgroup)
            grouproles = self._storage_engine.session.query(GroupRole).filter(GroupRole.group==dbgroup.name)
            for dbgrouprole in grouproles:
                group.add_role(dbgrouprole.role)
            usersgroupsauthorisor.groups[group.groupid] = group

        self.combine_users_and_groups(usersgroupsauthorisor)

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
