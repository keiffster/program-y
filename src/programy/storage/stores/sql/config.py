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
from programy.utils.logging.ylogger import YLogger

from programy.config.base import BaseConfigurationData
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.utils.substitutions.substitues import Substitutions


class SQLStorageConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="config")

        self._url = 'sqlite:///:memory:'
        self._echo = False
        self._encoding = 'utf-8'
        self._create_db = True
        self._drop_all_first = True

    @property
    def url(self):
        return self._url

    @property
    def echo(self):
        return self._echo

    @property
    def encoding(self):
        return self._encoding

    @property
    def create_db(self):
        return self._create_db

    @property
    def drop_all_first(self):
        return self._drop_all_first

    def check_for_license_keys(self, license_keys):
        BaseConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        storage = configuration_file.get_section(self._section_name, configuration)
        if storage is not None:
            self._url = configuration_file.get_option(storage, "url", subs=subs)
            if self._url.endswith("memory"):
                self._url += ":"
            self._echo = configuration_file.get_option(storage, "echo", subs=subs)
            self._encoding = configuration_file.get_option(storage, "encoding", subs=subs)
            self._create_db = configuration_file.get_option(storage, "create_db", subs=subs)
            self._drop_all_first = configuration_file.get_option(storage, "drop_all_first", subs=subs)

        else:
            YLogger.error(None, "'config' section missing from storage config")

    def create_sqlstorage_config(self):
        config = {}

        config['url'] = self._url
        config['echo'] = self._echo
        config['encoding'] = self._encoding
        config['create_db'] = self._create_db
        config['drop_all_first'] = self._drop_all_first

        if len(config.keys()) > 0:
            return config

        return None

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['url'] = 'sqlite:///:memory:'
            data['echo'] = False
            data['encoding'] = 'utf-8'
            data['create_db'] = True
            data['drop_all_first'] = True
        else:
            data['url'] = self._url
            data['echo'] = self._echo
            data['encoding'] = self._encoding
            data['create_db'] = self._create_db
            data['drop_all_first'] = self._drop_all_first

    def create_engine(self):
        engine = SQLStorageEngine(self)
        engine.initialise()
        return engine