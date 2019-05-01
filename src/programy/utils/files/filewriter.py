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
import datetime
import csv
import os


class TextFile(object):

    def __init__(self, filename, mode="a", encoding="utf-8"):
        self._filename = filename
        self._encoding = encoding
        self._file = open(self._filename, mode, encoding=self._encoding)

    @property
    def filename(self):
        return self._filename

    @property
    def encoding(self):
        return self._encoding


    def write_line(self, file_writer, elements):
        string = file_writer.format_row_as_text(elements)
        self._file.write(string)

    def flush(self):
        self._file.flush()


class CSVFile(object):

    def __init__(self, filename, mode="a", encoding="utf-8", delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
        self._filename = filename
        self._encoding = encoding
        self._file = open(self._filename, mode, encoding=self._encoding)
        self._csv_writer = csv.writer(self._file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)

    def write_line(self, _, elements):
        self._csv_writer.writerow(elements)

    def flush(self):
        return # Do nothing, noting to flush


class FileWriterConfiguration(object):

    def __init__(self, filename, file_format=None, mode="a", encoding="utf-8", delete_on_start=False):
        self._filename = filename
        self._file_format = file_format
        self._mode = mode
        self._encoding = encoding
        self._delete_on_start = delete_on_start

    @property
    def filename(self):
        return self._filename

    @property
    def file_format(self):
        return self._file_format

    @property
    def mode(self):
        return self._mode

    @property
    def encoding(self):
        return self._encoding

    @property
    def delete_on_start(self):
        return self._delete_on_start


class FileWriter(object):

    def __init__(self, configuration):
        self._filename = configuration.filename

        if configuration.delete_on_start:
            if os.path.exists(configuration.filename):
                YLogger.info(self, "Removing %s on start up", configuration.filename)
                os.remove(configuration.filename)

        if configuration.file_format == 'txt':
            self._file = TextFile(self._filename, encoding=configuration.encoding)

        elif configuration.file_format == 'csv':
            self._file = CSVFile(self._filename)
            self.write_header()

        else:
            raise Exception ("Unknown file type [%s]", configuration.file_format)

    def get_timestamp(self):
        return "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())


class ConversationFileWriter(FileWriter):

    def __init__(self, configuration):
        FileWriter.__init__(self, configuration)

    def log_question_and_answer(self, clientid, question, answer):
        row = [self.get_timestamp(), clientid, question, answer]
        self._file.write_line(self, row)
        self._file.flush()

    def format_row_as_text(self, row):
        return "%s - %s - Question[%s], Response[%s]\n"%(row[0], row[1], row[2], row[3])

    def write_header(self):
        self._file.write_line(self, ["Timestamp", "Clientid", "Question", "Response"])
        self._file.flush()


class ContentFileWriter(FileWriter):

    def __init__(self, configuration, content_type):
        FileWriter.__init__(self, configuration)
        self._content_type = content_type
        self._entries = []

    @property
    def entries(self):
        return self._entries

    def save_entry(self, content, filename,  startline, endline):
        timestamp = self.get_timestamp()
        if startline and endline:
            row = [timestamp, content, filename, startline, endline]
        else:
            row = [timestamp, content, filename]
        self._entries.append(row)

    def save_content(self):
        YLogger.info(self, "Saving aiml %s to file [%s]", self._content_type, self._filename )

        for entry in self._entries:
            self._file.write_line(self, entry)

        self._file.flush()
        return len(self._entries)

    def print_content(self):
        for entry in self._entries:
            print(entry)

    def format_row_as_text(self, row):
        if len(row) == 5:
            return "%s [%s] [%s] [%s] [%s]\n"%(row[0], row[1], row[2], row[3], row[4])
        else:
            return "%s [%s]\n"%(row[0], row[1])

    def display_debug_info(self):
        YLogger.info(self, "Found a total of %d %s in your grammrs, check out [%s] for details",
                         len(self._entries), self._content_type, self._filename)


class ErrorsFileWriter(ContentFileWriter):

    def __init__(self, configuration):
        ContentFileWriter.__init__(self, configuration, "errors")

    def write_header(self):
        self._file.write_line(self, ["Timestamp", "Error", "File", "Start Line", "End Line"])
        self._file.flush()


class DuplicatesFileWriter(ContentFileWriter):
    def __init__(self, configuration):
        ContentFileWriter.__init__(self, configuration, "duplicates")

    def write_header(self):
        self._file.write_line(self, ["Timestamp", "Duplicate", "File", "Start Line", "End Line"])
        self._file.flush()
