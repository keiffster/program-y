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
from abc import ABC
from abc import abstractmethod
from programy.utils.logging.ylogger import YLogger


class FileFinder(ABC):

    def __init__(self):
        pass    # pragma: no cover

    @abstractmethod
    def load_file_contents(self, fileid, filename, userid="*"):
        raise NotImplementedError()     # pragma: no cover

    def find_files(self, path, subdir=False, extension=None):
        found_files = []

        if subdir is False:
            paths = os.listdir(path)
            for filename in paths:
                if filename.endswith(extension):
                    found_files.append((filename, os.path.join(path, filename)))

        else:
            for dirpath, _, filenames in os.walk(path):
                for filename in [f for f in filenames if f.endswith(extension)]:
                    found_files.append((filename, os.path.join(dirpath, filename)))

        return sorted(found_files, key=lambda element: (element[1], element[0]))

    def load_dir_contents(self, paths, subdir=False, extension=".txt", filename_as_userid=False):

        files = self.find_files(paths, subdir, extension)

        collection = {}
        file_maps = {}
        for file in files:
            just_filename = FileFinder.get_just_filename_from_filepath(file[0])
            try:
                if filename_as_userid is True:
                    userid = just_filename

                else:
                    userid = "*"

                collection[just_filename.upper()] = self.load_file_contents(just_filename, file[1], userid=userid)
                file_maps[just_filename.upper()] = file[1]

            except Exception as excep:
                YLogger.exception(self, "Failed to load file contents for file [%s]", excep, file[1])

        return collection, file_maps

    def load_single_file_contents(self, filename):
        just_filename = FileFinder.get_just_filename_from_filepath(filename)

        collection = {}
        try:
            collection[just_filename] = self.load_file_contents(just_filename, filename)

        except Exception as excep:
            YLogger.exception(self, "Failed to load file contents for file [%s]", excep, filename)

        return collection

    @staticmethod
    def get_just_filename_from_filepath(filepath):

        if os.sep in filepath:
            pathsplits = filepath.split(os.sep)
            filename_ext = pathsplits[-1]
        else:
            filename_ext = filepath

        if "." in filename_ext:
            filesplits = filename_ext.split(".")
            filename = filesplits[0]
        else:
            filename = filename_ext

        return filename
