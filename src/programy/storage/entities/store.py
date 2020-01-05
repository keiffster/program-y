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
import os.path
from programy.storage.utils.processors import TextFile
from programy.storage.utils.processors import CSVFileReader
from programy.utils.logging.ylogger import YLogger


class Store:
    TEXT_FORMAT = "text"
    CSV_FORMAT = "csv"
    XML_FORMAT = "xml"
    BINARY_FORMAT = "bin"
    YAML_FORMAT = "yaml"

    def __init__(self):
        pass                # pragma: no cover

    def empty(self):
        return              # pragma: no cover

    def empty_named(self, name):
        del name            # pragma: no cover
        return              # pragma: no cover

    def commit(self, commit=True):
        return              # pragma: no cover

    def rollback(self, commit=True):
        return              # pragma: no cover

    def get_split_char(self):
        return ","

    def split_into_fields(self, line):
        return line.split(",")

    def process_line(self, name, fields, verbose=False):
        del name            # pragma: no cover
        del fields          # pragma: no cover
        del verbose         # pragma: no cover
        return False

    def upload_from_text(self, name, text, commit=True):
        try:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line)>0:
                    fields = self.split_into_fields(line)
                    self.process_line(name, fields)

            self.commit(commit)

        except Exception as e:
            YLogger.exception_nostack(self, "Error loading from text", e)
            self.rollback(commit)

    @staticmethod
    def get_file_processor(fileformat, filename):
        if fileformat == Store.TEXT_FORMAT:
            return TextFile(filename)
        elif fileformat == Store.CSV_FORMAT:
            return CSVFileReader(filename)
        else:
            raise Exception("Unknown file format [%s]" % fileformat)

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

    def upload_from_directory(self, directory, fileformat=TEXT_FORMAT, extension=None, subdir=True, commit=True,
                              verbose=False):

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
                                count, success = self.upload_from_file(fullpath, fileformat=fileformat, commit=commit,
                                                                       verbose=verbose)
                                final_count += count
                                final_success += success
                        else:
                            count, success = self.upload_from_file(fullpath, fileformat=fileformat, commit=commit,
                                                                   verbose=verbose)
                            final_count += count
                            final_success += success
            else:
                for dirpath, _, filenames in os.walk(directory):
                    for filename in filenames:
                        if extension is not None:
                            if filename.endswith(extension):
                                count, success = self.upload_from_file(os.path.join(dirpath, filename),
                                                                       fileformat=fileformat, commit=commit,
                                                                       verbose=verbose)
                                final_count += count
                                final_success += success
                        else:
                            count, success = self.upload_from_file(os.path.join(dirpath, filename),
                                                                   fileformat=fileformat, commit=commit,
                                                                   verbose=verbose)
                            final_count += count
                            final_success += success

            self.commit(commit)

        except Exception as e:
            YLogger.exception_nostack(self, "Error loading from directory", e)
            self.rollback(commit)

        return final_count, final_success

    def upload_from_file(self, filename, fileformat=TEXT_FORMAT, commit=True, verbose=False):

        file_processor = None
        final_count = 0
        final_success = 0
        try:
            name = Store.get_just_filename_from_filepath(filename)

            file_processor = Store.get_file_processor(fileformat, filename)
            count, success = file_processor.process_lines(name, self, verbose=verbose)
            final_count += count
            final_success += success

            self.commit(commit)

        except Exception as e:
            YLogger.exception_nostack(self, "Error uploading from file", e)
            self.rollback(commit=commit)

        finally:
            if file_processor is not None:
                file_processor.close()

        return final_count, final_success
