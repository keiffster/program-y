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

from abc import ABCMeta, abstractmethod


class BaseConfigurationData(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.section_name = name

    def _get_file_option(self, config_file, option_name, section, bot_root):
        option = config_file.get_option(section, option_name)
        if option is not None:
            option = self.sub_bot_root(option, bot_root)
        return option

    def sub_bot_root(self, text, root):
        return text.replace('$BOT_ROOT', root)

    @abstractmethod
    def load_config_section(self, config_file, bot_root):
        """
        Never Implemented
        """