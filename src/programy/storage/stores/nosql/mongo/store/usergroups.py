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

from programy.storage.entities.store import Store
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.usergroups import UserGroupsStore
from programy.storage.stores.nosql.mongo.dao.usergroups import UserGroups


class MongoUserGroupsStore(MongoStore, UserGroupsStore):

    USERGROUPS = 'usergroups'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoUserGroupsStore.USERGROUPS

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):

        YLogger.info(self, "Uploading usergroups from [%s] to Mongo", filename)

        usergroup_data = self._upload_usergroup_as_yaml(filename)

        collection = self.collection()
        usergroups = collection.find_one({})
        if usergroups is not None:
            usergroups.usergroups = usergroup_data
            collection.update(usergroups)
            YLogger.info(self, "Replacing existing usergroups in Mongo")
        else:
            usergroups = UserGroups(usergroup_data)
            self.add_document(usergroups)
            YLogger.info(self, "Adding new usergroups to Mongo")

        return 1, 1

    def load_usergroups(self, usersgroupsauthorisor):
        collection = self.collection()
        usergroups = collection.find_one({})
        if usergroups is not None:
            self.load_users_and_groups_from_yaml(usergroups['usergroups'], usersgroupsauthorisor)

    def _upload_usergroup_as_yaml(self, filename):

        try:
            with open(filename, 'r+', encoding="utf-8") as yaml_data_file:
                yaml_data = yaml.load(yaml_data_file, Loader=yaml.FullLoader)
                return yaml_data

        except Exception as e:
            YLogger.exception(self, "Failed to load usergroups yaml file [%s]", e, filename)

        return {}
