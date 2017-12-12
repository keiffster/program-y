"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import logging
import yaml

from programy.security.authorise.usergroups import User
from programy.security.authorise.usergroups import Group

class UserGroupLoader(object):

    def load_users_and_groups_from_text(self, text):
        yaml_data = yaml.load(text)
        if yaml_data is None:
            raise Exception("Yaml data is missing")
        return self.load_users_and_groups_from_yaml(yaml_data)

    def load_users_and_groups_from_file(self, filename):
        with open(filename, 'r+', encoding="utf-8") as yml_data_file:
            yaml_data = yaml.load(yml_data_file)
        return self.load_users_and_groups_from_yaml(yaml_data)

    def load_users_and_groups_from_yaml(self, yaml_data):
        users = self.load_users(yaml_data)
        groups = self.load_groups(yaml_data)
        self.combine_users_and_groups(users, groups)
        return users, groups

    def load_users(self, yaml_data):
        users = {}
        if 'users' in yaml_data:
            for user_name in yaml_data['users'].keys():

                user = User(user_name)

                yaml_obj = yaml_data['users'][user_name]
                if 'roles' in yaml_obj:
                    roles_list = yaml_obj['roles']
                    splits = roles_list.split(",")
                    for role_name in splits:
                        role_name = role_name.strip()
                        if role_name not in user.roles:
                            user.roles.append(role_name)
                        else:
                            if logging.getLogger().isEnabledFor(logging.DEBUG):
                                logging.debug("Role [%s] already exists in user [%s]", role_name, user_name)

                if 'groups' in yaml_obj:
                    groups_list = yaml_obj['groups']
                    splits = groups_list.split(",")
                    for group_name in splits:
                        group_name = group_name.strip()
                        if group_name not in user.groups:
                            user.groups.append(group_name)
                        else:
                            if logging.getLogger().isEnabledFor(logging.DEBUG):
                                logging.debug("Group [%s] already exists in user [%s]", group_name, user_name)

                users[user.userid] = user
        return users

    def load_groups(self, yaml_data):
        groups = {}
        if 'groups' in yaml_data:
            for group_name in yaml_data['groups'].keys():

                group = Group(group_name)

                yaml_obj = yaml_data['groups'][group_name]
                if 'roles' in yaml_obj:
                    roles_list = yaml_obj['roles']
                    splits = roles_list.split(",")
                    for role_name in splits:
                        role_name = role_name.strip()
                        if role_name not in group.roles:
                            group.roles.append(role_name)
                        else:
                            if logging.getLogger().isEnabledFor(logging.DEBUG):
                                logging.debug("Role [%s] already exists in group [%s]", role_name, group_name)

                if 'groups' in yaml_obj:
                    groups_list = yaml_obj['groups']
                    splits = groups_list.split(",")
                    for element in splits:
                        inner_group_name = element.strip()
                        if inner_group_name not in group.groups:
                            group.groups.append(inner_group_name)
                        else:
                            if logging.getLogger().isEnabledFor(logging.DEBUG):
                                logging.debug("Group [%s] already exists in group [%s]", inner_group_name, group_name)

                if 'users' in yaml_obj:
                    users_list = yaml_obj['groups']
                    splits = users_list.split(",")
                    for user_name in splits:
                        user_name = user_name.strip()
                        if user_name not in group.users:
                            group.users.append(user_name)
                        else:
                            if logging.getLogger().isEnabledFor(logging.DEBUG):
                                logging.debug("User [%s] already exists in group [%s]", user_name, group_name)

                groups[group.groupid] = group
        return groups

    def combine_users_and_groups(self, users, groups):

        for user_id in users.keys():
            user = users[user_id]

            new_groups = []
            for group_id in user.groups:
                if group_id in groups:
                    group = groups[group_id]
                    new_groups.append(group)
                else:
                    if logging.getLogger().isEnabledFor(logging.ERROR):
                        logging.error("Unknown group id [%s] in user [%s]", group_id, user_id)
            user.add_groups(new_groups[:])

        for group_id in groups.keys():
            group = groups[group_id]

            new_groups = []
            for sub_group_id in group.groups:
                if sub_group_id in groups:
                    new_group = groups[sub_group_id]
                    new_groups.append(new_group)
                else:
                    if logging.getLogger().isEnabledFor(logging.ERROR):
                        logging.error("Unknown group id [%s] in group [%s]", sub_group_id, group_id)
            group.add_groups(new_groups[:])

            new_users = []
            for sub_user_id in group.users:
                if sub_user_id in users:
                    new_user = users[sub_user_id]
                    new_users.append(new_user)
                else:
                    if logging.getLogger().isEnabledFor(logging.ERROR):
                        logging.error("Unknown user id [%s] in group [%s]", sub_user_id, group_id)
            group.add_users(new_users[:])

    def dump_users_and_groups(self, users, groups):

        if users is not None:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Users:")
            for user_id in users.keys():
                user = users[user_id]

                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("\t"+user.userid)

                if user.roles:
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        logging.debug("\t\tRoles:")
                    for role in user.roles:
                        if logging.getLogger().isEnabledFor(logging.DEBUG):
                            logging.debug("\t\t\t"+role)

                if user.groups:
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        logging.debug("\t\tGroups:")
                    for group in user.groups:
                        if logging.getLogger().isEnabledFor(logging.DEBUG):
                            logging.debug("\t\t\t" + group.groupid)

        if groups is not None:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Groups:")
            for group_id in groups.keys():
                group = groups[group_id]

                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("\t"+group.groupid)

                if group.roles:
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        logging.debug("\t\tRoles:")
                    for role in group.roles:
                        if logging.getLogger().isEnabledFor(logging.DEBUG):
                            logging.debug("\t\t\t"+role)

                if group.groups:
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        logging.debug("\t\tGroups:")
                    for group in group.groups:
                        if logging.getLogger().isEnabledFor(logging.DEBUG):
                            logging.debug("\t\t\t" + group.groupid)

                if group.users:
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        logging.debug("\t\tUsers:")
                    for user in group.users:
                        if logging.getLogger().isEnabledFor(logging.DEBUG):
                            logging.debug("\t\t\t" + user.userid)
