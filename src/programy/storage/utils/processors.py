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
import csv


class FileProcessor(object):

    READ = "r"
    WRITE = "w"
    EOL = "\n"
    UTF8 = "utf-8"

    def __init__(self, filename, mode="a", encoding=UTF8):
        self._filename = filename
        self._encoding = encoding
        self._mode = mode

    def flush(self):
        pass


class TextFile(FileProcessor):

    def __init__(self, filename, mode="r", encoding=FileProcessor.UTF8):
        FileProcessor.__init__(self, filename, mode, encoding)
        self._file = open(self._filename, self._mode, encoding=self._encoding)

    def close(self):
        self._file.close()

    def process_lines(self, set_name, processor, verbose=False):
        count = 0
        success = 0
        for line in self._file:
            line = line.strip(FileProcessor.EOL)
            fields = processor.split_into_fields(line)
            if processor.process_line(set_name, fields) is True:
                success += 1
            count += 1
        return count, success

    def write_line(self, file_writer, elements):
        string = file_writer.format_row_as_text(elements)
        self._file.write(string)

    def flush(self):
        self._file.flush()


class CSVFileProcessor(FileProcessor):

    DELIMITER = ','
    QUOTECHAR = '"'

    def __init__(self, filename, mode, encoding):
        FileProcessor.__init__(self, filename, mode, encoding)


class CSVFileWriter(CSVFileProcessor):

    def __init__(self, filename, mode=FileProcessor.WRITE, encoding=FileProcessor.UTF8, delimiter=CSVFileProcessor.DELIMITER, quotechar=CSVFileProcessor.QUOTECHAR, quoting=csv.QUOTE_ALL):
        CSVFileProcessor.__init__(self, filename, mode, encoding)
        self._file = open(self._filename, self._mode, encoding=self._encoding)
        self._csv_writer = csv.writer(self._file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)

    def write_line(self, _, elements):
        self._csv_writer.writerow(elements)

    def close(self):
        self._file.close()


class CSVFileReader(CSVFileProcessor):

    def __init__(self, filename, mode=FileProcessor.READ, encoding=FileProcessor.UTF8, delimiter=CSVFileProcessor.DELIMITER, quotechar=CSVFileProcessor.QUOTECHAR, quoting=csv.QUOTE_ALL):
        CSVFileProcessor.__init__(self, filename, mode, encoding)
        self._file = open(self._filename, self._mode, encoding=self._encoding)
        self._csv_reader = csv.reader(self._file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)

    def process_lines(self, name, processor):
        count = 0
        success = 0
        for line in self._csv_reader:
            if processor.process_line(name, line) is True:
                success += 1
            count += 1
        return count, success

    def close(self):
        self._file.close()
