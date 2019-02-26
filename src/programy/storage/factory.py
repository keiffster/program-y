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

class StorageFactory(object):

    USERS = "users"
    LINKED_ACCOUNTS = "linked_accounts"
    LINKS = "links"

    CATEGORIES = "categories"
    ERRORS = "errors"
    DUPLICATES = "duplicates"
    LEARNF = "learnf"
    CONVERSATIONS = "conversations"

    MAPS = "maps"
    SETS = "sets"
    RDF = "rdf"

    DENORMAL = "denormal"
    NORMAL = "normal"
    GENDER = "gender"
    PERSON = "person"
    PERSON2 = "person2"
    REGEX_TEMPLATES = "regex_templates"

    PROPERTIES = "properties"
    DEFAULTS = "defaults"
    VARIABLES = "variables"

    TWITTER = "twitter"

    SPELLING_CORPUS = "spelling_corpus"
    LICENSE_KEYS = "license_keys"

    TEMPLATE_NODES = "template_nodes"
    PATTERN_NODES = "pattern_nodes"

    BINARIES = "binaries"
    BRAINTREE = "braintree"

    PREPROCESSORS = "preprocessors"
    POSTPROCESSORS = "postprocessors"

    USERGROUPS = "usergroups"

    TRIGGERS = "triggers"

    def __init__(self):
        self._storage_engines = {}
        self._store_to_engine_map = {}

    def load_engines_from_config(self, configuration):
        for name, config in configuration.storage_configurations.items():
            try:
                self._storage_engines[name] = config.create_engine()
            except Exception as e:
                YLogger.exception(None, "Failed to create storage engine [%s]", e, name)

        for store_name, config in configuration.entity_store.items():
            if config in self._storage_engines:
                self._store_to_engine_map[store_name] = self._storage_engines[config]
            else:
                YLogger.error(self, "%s is not a valid storage engine name", config)

    def storage_engine_available(self, name):
        return name in self._storage_engines

    def storage_engine(self, name):
        if self.storage_engine_available(name):
            return self._storage_engines[name]
        else:
            return None

    def entity_storage_engine_available(self, entity_name):
        return entity_name in self._store_to_engine_map

    def entity_storage_engine(self, entity_name):
        if self.entity_storage_engine_available(entity_name):
            return self._store_to_engine_map[entity_name]
        else:
            return None
