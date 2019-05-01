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
from abc import ABCMeta
from programy.utils.logging.ylogger import YLogger
from programy.utils.substitutions.substitues import Substitutions

class BaseConfigurationData(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):

        assert (name is not None)

        self._section_name = name
        self._additionals = {}

    def exists(self, name):

        assert (name is not None)

        return bool(name in self._additionals)

    def value(self, key):

        assert (key is not None)

        if key in self._additionals:
            return self._additionals[key]

        else:
            YLogger.warning(self, "Configuration key [%s] does not exist", key)

        return None

    @property
    def section_name(self):
        return self._section_name

    @property
    def id(self):
        return self._section_name

    def _get_file_option(self, config_file, option_name, section, bot_root, subs: Substitutions=None):

        assert (config_file is not None)
        assert (option_name is not None)

        option = config_file.get_option(section, option_name, subs=subs)
        if option is not None:
            option = self.sub_bot_root(option, bot_root, subs=subs)
        return option

    def sub_bot_root(self, text, root):

        assert text is not None
        assert root is not None

        return text.replace('$BOT_ROOT', root)

    def additionals_to_add(self):
        return []

    def load_additional_key_values(self, configuration, section, subs: Substitutions = None):
        if configuration:
            if section is not None:
                for key in configuration.get_keys(section):
                    if key in self.additionals_to_add():
                        value = configuration.get_option(section, key, subs=subs)
                        self._additionals[key] = value

    def _extract_license_key(self, attr, license_keys):
        if attr is not None:
            if "LICENSE:" in attr:
                if license_keys.has_key(attr[8:]):
                    return license_keys.get_key(attr[8:])
        return attr

    def check_for_license_keys(self, license_keys):
        return

    def config_to_yaml(self, data, config, defaults=True):

        assert (data is not None)
        assert (config is not None)

        data[config.id] = {}
        config.to_yaml(data[config.id], defaults)

    def to_yaml(self, data, defaults=True):
        pass
