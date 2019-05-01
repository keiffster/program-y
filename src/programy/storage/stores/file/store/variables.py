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

import os
import os.path
import shutil

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.variables import VariablesStore

class FileVariablesStore(FileStore, VariablesStore):

    SPLIT_CHAR = ':'
    COMMENT = '#'

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self._storage_engine.configuration.variables_storage.dirs[0]

    def empty(self):
        vars_path = self._get_storage_path()
        if os.path.exists(vars_path) is True:
            shutil.rmtree(vars_path)

    def empty_variables(self, clientid, userid):
        variables_filepath = self._variables_filename(self._get_storage_path(), clientid, userid)
        if os.path.exists(variables_filepath):
            os.remove(variables_filepath)

    def add_variable(self, clientid, userid, name, value):

        vars_path = self._get_storage_path()
        self._ensure_dir_exists(vars_path)

        variables_filepath = self._variables_filename(vars_path, clientid, userid)

        variables = self._load_variables(variables_filepath)

        variables[name] = value

        self._write_variables(variables_filepath, variables)

    def add_variables(self, clientid, userid, variables):

        vars_path = self._get_storage_path()
        self._ensure_dir_exists(vars_path)

        variables_filepath = self._variables_filename(vars_path, clientid, userid)

        self._write_variables(variables_filepath, variables)

    def get_variables(self, clientid, userid):
        self._ensure_dir_exists(self._get_storage_path())
        variables_filepath = self._variables_filename(self._get_storage_path(), clientid, userid)
        variables = self._load_variables(variables_filepath)
        return variables

    def _variables_filename(self, storage_dir, clientid, userid, ext="vars"):
        return "%s%s%s_%s.%s"%(storage_dir, os.sep, clientid, userid, ext)

    def _load_variables(self, variables_filepath):
        variables = {}
        if os.path.exists(variables_filepath):
            try:
                with open(variables_filepath, "r") as vars_file:
                    for line in vars_file:
                        line = line.strip()
                        if line:
                            if line.startswith(FileVariablesStore.COMMENT) is False:
                                splits = line.split(FileVariablesStore.SPLIT_CHAR)
                                if len(splits)>1:
                                    key = splits[0].strip()
                                    val = splits[1].strip()
                                    variables[key] = val

            except Exception as e:
                YLogger.exception_nostack(None, "Failed to load variables [%s]", e, variables_filepath)

        return variables

    def _write_variables(self, variables_filepath, variables):
        try:
            with open(variables_filepath, "w+") as vars_file:
                for key, value in variables.items():
                    vars_file.write("%s%s%s\n"%(key, FileVariablesStore.SPLIT_CHAR, value))
                vars_file.write("\n")

        except Exception as e:
            YLogger.exception_nostack(None, "Failed to write variables [%s]", e, variables_filepath)

    def _load_file_contents(self, collection, filename):
        variables = self._load_variables(filename)
        for key, value in variables.items():
            collection.add_property(key, value)

    def get_storage(self):
        return self.storage_engine.configuration.variables_storage