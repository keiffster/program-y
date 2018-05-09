"""
Copyright(c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files(the "Software"), to deal in the Software without restriction, including without limitation
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
from programy.utils.files.filefinder import FileFinder


class SetLoader(FileFinder):
    def __init__(self):
        FileFinder.__init__(self)

    def sort_sets(self, the_set):
        sorted_set = {}
        for key in the_set.keys():
            values = the_set[key]
            sorted_values = sorted(values, key=len, reverse=True)
            sorted_set[key] = sorted_values
        return sorted_set

    def load_file_contents(self, id, filename, userid="*"):
        YLogger.debug(self, "Loading set [%s]", filename)
        the_set = {}
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    self.process_line(line, the_set)
        except Exception as excep:
            YLogger.error(self, "Failed to load set [%s] - %s", filename, excep)
        return self.sort_sets(the_set)

    def load_from_text(self, text):
        the_set = {}
        lines = text.split("\n")
        for line in lines:
            self.process_line(line, the_set)
        return self.sort_sets(the_set)

    def process_line(self, line, the_set):
        text = line.strip()
        if text is not None and text:
            splits = text.split()
            key = splits[0].upper()
            if key not in the_set:
                the_set[key] = []
            the_set[key].append(splits)


class SetCollection(object):

    def __init__(self):
        self._sets = {}
        self._files = {}

    def empty(self):
        self._sets.clear()
        self._files.clear()

    def add_set(self, name, the_set):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        if set_name in self._sets:
            raise Exception("Set %s already exists" % set_name)
        YLogger.debug(self, "Adding set [%s[ to set group", set_name)
        self._sets[set_name] = the_set

    def set(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        return self._sets[set_name]

    def filename(self, setname):
        return self._files[setname]

    def contains(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        return bool(set_name in self._sets)

    def count_words_in_sets(self):
        count = 0
        for aset in self._sets.values():
            count += len(aset)
        return count

    def load(self, configuration):
        loader = SetLoader()
        if configuration.files is not None:
            self._sets = {}
            for file in configuration.files:
                sets, file_sets = loader.load_dir_contents(file, configuration.directories, configuration.extension)
                for key in sets.keys():
                    if key in self._sets:
                        YLogger.error(self, "Duplicate set [%s] found in [%s]", key, file)
                    self._sets[key] = sets[key]
                for key in file_sets.keys():
                    self._files[key] = file_sets[key]
        else:
            self._sets = {}
        return len(self._sets)

    def reload_file(self, filename):
        loader = SetLoader()
        just_filename = loader.get_just_filename_from_filepath(filename)
        new_set = loader.load_file_contents(just_filename, filename)
        set_name = just_filename.upper()
        del self._sets[set_name]
        self._sets[set_name] = new_set
