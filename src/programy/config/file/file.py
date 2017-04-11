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


class BaseConfigurationFile(object):
    __metaclass__ = ABCMeta

    def __init__(self, client_config):
        self.client_config = client_config

    @abstractmethod
    def load_from_text(self, text, bot_root):
        """
        Never Implemented
        """

    @abstractmethod
    def load_from_file(self, filename, bot_root):
        """
        Never Implemented
        """

    @abstractmethod
    def get_section(self, section_name, parent_section=None):
        """
        Never Implemented
        """

    @abstractmethod
    def get_section_data(self, section_name, parent_section=None):
        """
        Never Implemented
        """

    @abstractmethod
    def get_child_section_keys(self, section_name, parent_section=None):
        """
        Never Implemented
        """

    @abstractmethod
    def get_option(self, section, option_name, missing_value=None):
        """
        Never Implemented
        """

    def _infer_type_from_string(self, text):
        if text == 'True' or text == 'true':
            return True
        elif text == 'False' or text == 'false':
            return False
        else:
            return text
