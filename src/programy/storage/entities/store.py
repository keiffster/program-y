"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
import os.path

from programy.storage.utils.processors import TextFile
from programy.storage.utils.processors import CSVFileReader

class Store(object):

    CSV_FORMAT = "csv"
    TEXT_FORMAT = "text"

    def empty(self):
        raise NotImplementedError("empty missing from implementation")

    def empty_named(self, name):
        raise NotImplementedError("empty_named missing from implementation")

    def upload_from_text(self, name, text, commit=True):

        self.empty_named(name)

        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                fields = self.split_into_fields(line)
                self.process_line(name, fields)

        if commit is True:
            self.commit()

    @staticmethod
    def get_file_processor(format, filename):
        if format == Store.TEXT_FORMAT:
            print("Processing text file")
            return TextFile(filename)
        elif format == Store.CSV_FORMAT:
            print("Processing csv file")
            return CSVFileReader(filename)
        else:
            raise Exception("Unknown file format [%s]" % format)

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

        return filename.upper()

    def upload_from_file(self, filename, format=TEXT_FORMAT, commit=True):
        try:
            print("Load from file [%s]"%filename)
            name = self.get_just_filename_from_filepath(filename)
            self.empty_named(name)

            file_processor = self.get_file_processor(format, filename)
            file_processor.process_lines(name, self)

            if commit is True:
                self.commit()

        except Exception as e:
            print(e)
            if commit is True:
                self.rollback()

    def upload_from_directory(self, directory, format=TEXT_FORMAT, extension=None, subdir=True, commit=True):

        try:
            if subdir is False:
                paths = os.listdir(directory)
                for filename in paths:
                    if extension is not None:
                        if filename.endswith(extension):
                            self.upload_from_file(os.path.join(directory, filename), format=format, commit=False)
                    else:
                        self.upload_from_file(os.path.join(directory, filename), format=format, commit=False)
            else:
                for dirpath, _, filenames in os.walk(directory):
                    for filename in filenames:
                        if extension is not None:
                            if filename.endswith(extension):
                                self.upload_from_file(os.path.join(dirpath, filename), format=format, commit=False)
                        else:
                            self.upload_from_file(os.path.join(dirpath, filename), format=format, commit=False)

            if commit is True:
                self.commit()

        except Exception as e:
            print(e)
            if commit is True:
                self.rollback()
