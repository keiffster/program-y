"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
from programy.utils.files.filefinder import FileFinder
from programy.mappings.base import SingleStringCollection

class SetLoader(FileFinder):
    def __init__(self):
        FileFinder.__init__(self)

    def load_file_contents(self, filename):
        logging.debug("Loading set [%s]" % filename)
        the_set = []
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    self.process_line(line, the_set)
        except Exception as e:
            logging.error("Failed to load set [%s] - %s"%(filename, e))
        return the_set

    def load_from_text(self, text):
        the_set = []
        lines = text.split("\n")
        for line in lines:
            self.process_line(line, the_set)
        return the_set

    def process_line(self, line, the_set):
        text = line.strip()
        if text is not None and len(text) > 0:
            value = text.upper ()
            the_set.append(value)


class SetCollection(object):

    def __init__(self):
        SingleStringCollection.__init__(self)
        self._sets = {}

    def add_set(self, name, set_contents):
        set_name = name.upper()
        if set_name in self._sets:
            raise Exception("Set %s already exists" % set_name)
        logging.debug("Adding set [%s[ to set group" % set_name)
        self._sets[set_name] = set_contents

    def set(self, name):
        set_name = name.upper ()
        return self._sets[set_name]

    def contains(self, name):
        set_name = name.upper ()
        if set_name in self._sets:
            return True
        else:
            return False

    def count_words_in_sets(self):
        count = 0
        for aset in self._sets.values():
            count += len(aset)
        return count

    def load(self, configuration):
        loader = SetLoader ()
        self._sets = loader.load_dir_contents(configuration.files, configuration.directories, configuration.extension)
        return len(self._sets)