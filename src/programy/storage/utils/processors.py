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
import csv


class FileProcessor(object):

    def __init__(self, filename, mode="a", encoding="utf-8"):
        self._filename = filename
        self._encoding = encoding
        self._mode = mode

    def flush(self):
        pass


class TextFile(FileProcessor):

    def __init__(self, filename, mode="r", encoding="utf-8"):
        FileProcessor.__init__(self, filename, mode, encoding)
        self._file = open(self._filename, self._mode, encoding=self._encoding)

    def process_lines(self, set_name, processor):
        for line in self._file:
            line = line.strip('\n')
            fields = processor.split_into_fields(line)
            processor.process_line(set_name, fields)

    def write_line(self, file_writer, elements):
        string = file_writer.format_row_as_text(elements)
        self._file.write(string)

    def flush(self):
        self._file.flush()


class CSVFileWriter(FileProcessor):

    def __init__(self, filename, mode="r", encoding="utf-8", delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
        FileProcessor.__init__(self, filename, mode, encoding)
        self._file = open(self._filename, self._mode, encoding=self._encoding)
        self._csv_writer = csv.writer(self._file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)

    def write_line(self, _, elements):
        self._csv_writer.writerow(elements)


class CSVFileReader(FileProcessor):

    def __init__(self, filename, mode="r", encoding="utf-8", delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
        FileProcessor.__init__(self, filename, mode, encoding)
        self._file = open(self._filename, self._mode, encoding=self._encoding)
        self._csv_reader = csv.reader(self._file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)

    def process_lines(self, name, processor):
        for line in self._csv_reader:
            processor.process_line(name, line)
