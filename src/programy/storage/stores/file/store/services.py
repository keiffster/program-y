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
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.services import ServicesStore
from programy.services.config import ServiceConfiguration


class FileServiceStore(FileStore, ServicesStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        ServicesStore.__init__(self)

    def _get_storage_path(self):
        return self.storage_engine.configuration.services_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.services_storage

    def load_all(self, collector):
        dirs = self.storage_engine.configuration.services_storage.dirs
        cat_ext = self.storage_engine.configuration.services_storage.extension
        subdirs = self.storage_engine.configuration.services_storage.subdirs

        if self.storage_engine.configuration.services_storage.has_single_file():
            for filename in dirs:
                if cat_ext is not None:
                    if filename.endswith(cat_ext):
                        self._load_file_contents(collector, filename)

                else:
                    self._load_file_contents(collector, filename)
        else:
            for cat_dir in dirs:
                if os.path.isfile(cat_dir):
                    self._load_file_contents(collector, cat_dir)

                elif subdirs is False:
                    if os.path.exists(cat_dir):
                        paths = os.listdir(cat_dir)
                        for filename in paths:
                            if cat_ext is not None:
                                if filename.endswith(cat_ext):
                                    self._load_file_contents(collector, os.path.join(cat_dir, filename))
                            else:
                                self._load_file_contents(collector, os.path.join(cat_dir, filename))

                    else:
                        YLogger.error(self, "Error loading Service config file [%s]", cat_dir)

                else:
                    if os.path.exists(cat_dir):
                        for dirpath, _, filenames in os.walk(cat_dir):
                            for filename in [f for f in filenames if f.endswith(cat_ext)]:
                                self._load_file_contents(collector, os.path.join(dirpath, filename))
                    else:
                        YLogger.error(self, "Error loading Service config file [%s]", cat_dir)

    def _load_file_contents(self, handler, filename):
        YLogger.debug(self, "Loading services from file [%s]", filename)
        count = 0
        try:
            with open(filename, "r", encoding="utf-8") as file:
                self._process_service_yaml(handler, file, filename)
                count += 1

        except Exception as error:
            YLogger.exception(self, "Error loading Service config file [%s]", error, filename)

        return count

    def _process_service_yaml(self, handler, file, filename):
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)

        configuration = ServiceConfiguration.new_from_yaml(yaml_data, filename)

        return handler.load_service(configuration)
