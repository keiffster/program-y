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
import os
import os.path

from programy.storage.utils.processors import TextFile
from programy.storage.utils.processors import CSVFileReader

class Store(object):

    TEXT_FORMAT = "text"
    CSV_FORMAT = "csv"
    XML_FORMAT = "xml"
    BINARY_FORMAT = "bin"
    YAML_FORMAT = "yaml"

    def store_name(self):
        raise NotImplementedError

    def empty(self):
        raise NotImplementedError("empty missing from implementation")

    def empty_named(self, name):
        raise NotImplementedError("empty_named missing from implementation")

    def upload_from_text(self, name, text, commit=True):
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
            return TextFile(filename)
        elif format == Store.CSV_FORMAT:
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

    def upload_from_directory(self, directory, format=TEXT_FORMAT, extension=None, subdir=True, commit=True, verbose=False):

        final_count = 0
        final_success = 0

        try:
            if subdir is False:
                paths = os.listdir(directory)
                for filename in paths:
                    fullpath = os.path.join(directory, filename)
                    if os.path.isdir(fullpath) is False:
                        if extension is not None:
                            if filename.endswith(extension):
                                count, success = self.upload_from_file(fullpath, format=format, commit=commit, verbose=verbose)
                                final_count += count
                                final_success += success
                        else:
                            count, success = self.upload_from_file(fullpath, format=format, commit=commit, verbose=verbose)
                            final_count += count
                            final_success += success
            else:
                for dirpath, _, filenames in os.walk(directory):
                    for filename in filenames:
                        if extension is not None:
                            if filename.endswith(extension):
                                count, success = self.upload_from_file(os.path.join(dirpath, filename), format=format, commit=commit, verbose=verbose)
                                final_count += count
                                final_success += success
                        else:
                            count, success = self.upload_from_file(os.path.join(dirpath, filename), format=format, commit=commit, verbose=verbose)
                            final_count += count
                            final_success += success

            if commit is True:
                self.commit()

        except Exception as e:
            print("Error loading from directory", e)
            if commit is True:
                self.rollback()

        return final_count, final_success

    def upload_from_file(self, filename, format=TEXT_FORMAT, commit=True, verbose=False):

        file_processor = None
        final_count = 0
        final_success = 0
        try:
            name = self.get_just_filename_from_filepath(filename)
            print(name)

            file_processor = Store.get_file_processor(format, filename)
            count, success = file_processor.process_lines(name, self, verbose=verbose)
            final_count += count
            final_success += success

            if commit is True:
                self.commit()

        except Exception as e:
            print("Error uploading from file: ", e)
            if commit is True:
                self.rollback()

        finally:
            if file_processor is not None:
                file_processor.close()

        return final_count, final_success