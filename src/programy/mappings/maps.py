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

class MapLoader(FileFinder):
    def __init__(self):
        FileFinder.__init__(self)

    def load_file_contents(self, filename):
        the_map = {}
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    self.process_line(line, the_map)
        except Exception as e:
            logging.error("Failed to load map [%s] - %s"%(filename, e))
        return the_map

    def load_from_text(self, text):
        the_map = {}
        lines = text.split("\n")
        for line in lines:
            self.process_line(line, the_map)
        return the_map

    def process_line(self, line, the_map):
        text = line.strip()
        if text is not None and len(text) > 0:
            splits = text.split(":")
            the_map[splits[0]] = splits[1]


class MapCollection(object):

    def __init__(self):
        self._maps = {}

    def map(self, name):
        return self._maps[name]

    def contains(self, name):
        if name in self._maps.keys():
            return True
        else:
            return False

    def load(self, configuration):

        loader = MapLoader ()
        self._maps = loader.load_dir_contents(configuration.files, configuration.directories, configuration.extension)

        return len(self._maps)