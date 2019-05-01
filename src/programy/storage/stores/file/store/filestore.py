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

from programy.storage.entities.store import Store

class FileStore(Store):

    FILE = "file"

    CATEGORIES_STORAGE = 'categories_storage'
    ERRORS_STORAGE = 'errors_storage'
    DUPLICATES_STORAGE = 'duplicates_storage'
    LEARNF_STORAGE = 'learnf_storage'

    CONVERSATION_STORAGE = 'conversation_storage'

    SETS_STORAGE = 'sets_storage'
    MAPS_STORAGE = 'maps_storage'
    RDF_STORAGE = 'rdf_storage'

    DENORMAL_STORAGE = 'denormal_storage'
    NORMAL_STORAGE = 'normal_storage'
    GENDER_STORAGE = 'gender_storage'
    PERSON_STORAGE = 'person_storage'
    PERSON2_STORAGE = 'person2_storage'
    REGEX_STORAGE = 'regex_storage'

    PROPERTIES_STORAGE = 'properties_storage'
    VARIABLES_STORAGE = 'variables_storage'
    DEFAULTS_STORAGE = 'defaults_storage'

    TWITTER_STORAGE = 'twitter_storage'

    SPELLING_STORAGE = 'spelling_storage'

    LICENSE_STORAGE = 'license_storage'

    PATTERN_NODES_STORAGE = 'pattern_nodes_storage'
    TEMPLATE_NODES_STORAGE = 'template_nodes_storage'

    BINARIES_STORAGE = 'binaries_storage'
    BRAINTREE_STORAGE = 'braintree_storage'

    PREPROCESSORS_STORAGE = 'preprocessors_storage'
    POSTPROCESSORS_STORAGE = 'postprocessors_storage'

    USERGROUPS_STORAGE = 'usergroups_storage'

    TRIGGERS_STORAGE = 'triggers_storage'

    def __init__(self, storage_engine):
        self._storage_engine = storage_engine

    def store_name(self):
        return FileStore.FILE

    def empty(self):
        pass

    def empty_named(self, name):
        pass

    @property
    def storage_engine(self):
        return self._storage_engine

    def _get_storage_path(self):
        raise NotImplementedError("Implement _get_storage_path to return storage specific folder from config")

    def drop(self):
        try:
            storage_path = self._get_storage_path()
            if os.path.exists(storage_path):
                shutil.rmtree(storage_path)
        except Exception as e:
            YLogger.exception_nostack(self, "Error dropping storage", e)

    @staticmethod
    def _get_dir_from_path(file_path):
        splits = file_path.split(os.sep)
        paths = splits[:len(splits)-1]
        path = "/".join(paths)
        return path

    @staticmethod
    def _ensure_dir_exists(path):
        if os.path.exists(path) is False:
            YLogger.debug(None, "Directory does not exist, creating %s", path)
            os.makedirs(path)

    @staticmethod
    def _file_exists(path):
        return os.path.exists(path)

    def commit(self):
        pass

    def load_all(self, collection):
        col_storage = self.get_storage()

        if col_storage.has_multiple_dirs():
            subdir = col_storage.subdirs
            col_ext = col_storage.extension
            for col_dir in col_storage.dirs:
                if subdir is False:
                    paths = os.listdir(col_dir)
                    for filename in paths:
                        if col_ext is None or filename.endswith(col_ext):
                            YLogger.debug(self, "Loading file contents from [%s]", filename)
                            self._load_file_contents(collection, os.path.join(col_dir, filename))
                else:
                    for dirpath, _, filenames in os.walk(col_dir):
                        for filename in [f for f in filenames if f.endswith(col_ext)]:
                            YLogger.debug(self, "Loading file contents from [%s]", filename)
                            self._load_file_contents(collection, os.path.join(dirpath, filename))

        else:
            self.load(collection)

    def load(self, collection):
        col_storage = self.get_storage()
        collection.empty()
        self._load_file_contents(collection, col_storage.file)

    def _load_file_contents(self, processor_collection, filename):
        pass

    def get_storage(self):
        raise NotImplementedError("get_storage must be implemented in child class")

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):

        YLogger.debug(self, "Oploading from file [%s]", filename)

        file_processor = None
        try:
            name = self.get_just_filename_from_filepath(filename)
            if verbose is True:
                print(name)

            file_processor = self.get_file_processor(format, filename)
            file_processor.process_lines(name, self, verbose=verbose)

            if commit is True:
                self.commit()

        except Exception as e:
            YLogger.exception_nostack(self, "Error uploading from file [%s]", e, filename)

            if commit is True:
                self.rollback()

        finally:
            if file_processor is not None:
                file_processor.close()

