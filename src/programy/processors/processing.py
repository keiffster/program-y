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

from programy.utils.logging.ylogger import YLogger
from abc import ABCMeta, abstractmethod

from programy.utils.classes.loader import ClassLoader

class ProcessorLoader(ClassLoader):

    def __init__(self):
        ClassLoader.__init__(self)
        self.processors = []

    def empty(self):
        self.processors.clear()

    def load(self, filename, *args, **kw):
        YLogger.debug(self, "Loading processors from file [%s]", filename)
        count = 0
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if line[0] != '#':
                            new_class = ClassLoader.instantiate_class(line)
                            if new_class is not None:
                                self.processors.append(new_class(*args, **kw))
                                count += 1
        except FileNotFoundError:
            YLogger.error(self, "File not found [%s]", filename)
        return count

    def process(self, client_context, string):
        for processor in self.processors:
            string = processor.process(client_context, string)
        return string


##################################################################
#
class Processor:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def process(self, client_context, word_string):
        pass


##################################################################
#
class PreProcessor(Processor):

    def __init__(self):
        Processor.__init__(self)

    @abstractmethod
    def process(self, client_context, word_string):
        pass

##################################################################
#
class PostProcessor(Processor):
    def __init__(self):
        Processor.__init__(self)

    @abstractmethod
    def process(self, client_context, word_string):
        pass
