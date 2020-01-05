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
from programy.utils.logging.ylogger import YLogger
from programy.security.authorise.usergroups import User
from programy.security.authorise.usergroups import Group
from programy.storage.entities.store import Store


class UserGroupsStore(Store):

    def __init__(self):
        Store.__init__(self)

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):
        raise NotImplementedError()  # pragma: no cover

    def load_usergroups(self, usersgroupsauthorisor):
        raise NotImplementedError()  # pragma: no cover

    def load_users_and_groups_from_yaml(self, yaml_data, usergroups):
        self._load_users(yaml_data, usergroups)
        self._load_groups(yaml_data, usergroups)
        self._combine_users_and_groups(usergroups)

    def _load_users(self, yaml_data, usergroups):
        if 'users' in yaml_data:
            for user_name in yaml_data['users'].keys():
                self._load_users_user(yaml_data, user_name, usergroups)

    def _load_users_user(self, yaml_data, user_name, usergroups):
        user = User(user_name)

        yaml_obj = yaml_data['users'][user_name]
        if 'roles' in yaml_obj:
            self._load_users_user_roles(yaml_obj, user, user_name)

        if 'groups' in yaml_obj:
            self._load_users_user_groups(yaml_obj, user, user_name)

        usergroups.users[user.userid] = user

    def _load_users_user_roles(self, yaml_obj, user, user_name):
        roles_list = yaml_obj['roles']
        splits = roles_list.split(",")
        for role_name in splits:
            role_name = role_name.strip()
            if role_name not in user.roles:
                user.roles.append(role_name)
            else:
                YLogger.debug(self, "Role [%s] already exists in user [%s]", role_name, user_name)

    def _load_users_user_groups(self, yaml_obj, user, user_name):
        groups_list = yaml_obj['groups']
        splits = groups_list.split(",")
        for group_name in splits:
            group_name = group_name.strip()
            if group_name not in user.groups:
                user.groups.append(group_name)
            else:
                YLogger.debug(self, "Group [%s] already exists in user [%s]", group_name, user_name)

    def _load_groups(self, yaml_data, usergroups):
        if 'groups' in yaml_data:
            for group_name in yaml_data['groups'].keys():
                self._load_groups_group(yaml_data, group_name, usergroups)

    def _load_groups_group(self, yaml_data, group_name, usergroups):
        group = Group(group_name)

        yaml_obj = yaml_data['groups'][group_name]
        if 'roles' in yaml_obj:
            self._load_groups_group_roles(yaml_obj, group, group_name)

        if 'groups' in yaml_obj:
            self._load_groups_group_groups(yaml_obj, group, group_name)

        if 'users' in yaml_obj:
            self._load_groups_group_users(yaml_obj, group, group_name)

        usergroups.groups[group.groupid] = group

    def _load_groups_group_roles(self, yaml_obj, group, group_name):
        roles_list = yaml_obj['roles']
        splits = roles_list.split(",")
        for role_name in splits:
            role_name = role_name.strip()
            if role_name not in group.roles:
                group.roles.append(role_name)
            else:
                YLogger.debug(self, "Role [%s] already exists in group [%s]", role_name, group_name)

    def _load_groups_group_groups(self, yaml_obj, group, group_name):
        groups_list = yaml_obj['groups']
        splits = groups_list.split(",")
        for element in splits:
            inner_group_name = element.strip()
            if inner_group_name not in group.groups:
                group.groups.append(inner_group_name)
            else:
                YLogger.debug(self, "Group [%s] already exists in group [%s]", inner_group_name, group_name)

    def _load_groups_group_users(self, yaml_obj, group, group_name):
        users_list = yaml_obj['users']
        splits = users_list.split(",")
        for user_name in splits:
            user_name = user_name.strip()
            if user_name not in group.users:
                group.users.append(user_name)
            else:
                YLogger.debug(self, "User [%s] already exists in group [%s]", user_name, group_name)

    def _combine_users_and_groups(self, usergroups):

        for user_id in usergroups.users.keys():
            user = usergroups.users[user_id]
            self._combine_user_groups(usergroups, user, user_id)

        for group_id in usergroups.groups.keys():
            group = usergroups.groups[group_id]
            self._combine_group_groups(usergroups, group, group_id)
            self._combine_group_users(usergroups, group, group_id)

    def _combine_user_groups(self, usergroups, user, user_id):
        new_groups = []
        for group_id in user.groups:
            if group_id in usergroups.groups:
                group = usergroups.groups[group_id]
                new_groups.append(group)
            else:
                YLogger.error(self, "Unknown group id [%s] in user [%s]", group_id, user_id)
        user.add_groups(new_groups[:])

    def _combine_group_groups(self, usergroups, group, group_id):
        new_groups = []
        for sub_group_id in group.groups:
            if sub_group_id in usergroups.groups:
                new_group = usergroups.groups[sub_group_id]
                new_groups.append(new_group)
            else:
                YLogger.error(self, "Unknown group id [%s] in group [%s]", sub_group_id, group_id)
        group.add_groups(new_groups[:])

    def _combine_group_users(self, usergroups, group, group_id):
        new_users = []
        for sub_user_id in group.users:
            if sub_user_id in usergroups.users:
                new_user = usergroups.users[sub_user_id]
                new_users.append(new_user)
            else:
                YLogger.error(self, "Unknown user id [%s] in group [%s]", sub_user_id, group_id)
        group.add_users(new_users[:])

