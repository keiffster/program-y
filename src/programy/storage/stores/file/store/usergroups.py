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

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.usergroups import UserGroupsStore
import yaml


class FileUserGroupStore(FileStore, UserGroupsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def load_usergroups(self, usersgroupsauthorisor):
        filename = self.get_storage().file

        try:
            with open(filename, 'r+', encoding=self.get_storage().encoding) as yml_data_file:
                yaml_data = yaml.load(yml_data_file, Loader=yaml.FullLoader)

            self.load_users_and_groups_from_yaml(yaml_data, usersgroupsauthorisor)

        except Exception as e:
            YLogger.exception_nostack(self, "Failed to load usergroups yaml file [%s]", e, filename)


    def get_storage(self):
        return self.storage_engine.configuration.usergroups_storage
