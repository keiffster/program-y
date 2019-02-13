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

from programy.config.file.xml_file import XMLConfigurationFile
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.file.json_file import JSONConfigurationFile
from programy.utils.substitutions.substitues import Substitutions


class ConfigurationFactory(object):

    @classmethod
    def load_configuration_from_file(cls, client_configuration, filename, file_format=None, bot_root=".", subs: Substitutions = None):

        if file_format is None or not file_format:
            file_format = ConfigurationFactory.guess_format_from_filename(filename)

        config_file = ConfigurationFactory.get_config_by_name(file_format)
        return config_file.load_from_file(filename, client_configuration, bot_root, subs)

    @classmethod
    def guess_format_from_filename(cls, filename):
        if "." not in filename:
            raise Exception("No file extension to allow format guessing!")

        last_dot = filename.rfind(".")
        file_format = filename[last_dot + 1:]
        return file_format

    @classmethod
    def get_config_by_name(cls, file_format):
        file_format = file_format.lower()

        if file_format == 'yaml':
            return YamlConfigurationFile()
        elif file_format == 'json':
            return JSONConfigurationFile()
        elif file_format == 'xml':
            return XMLConfigurationFile()
        else:
            raise Exception("Unsupported configuration format:", file_format)
