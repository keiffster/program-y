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

from pymongo import MongoClient

from programy.storage.engine import StorageEngine

from programy.storage.stores.nosql.mongo.store.categories import MongoCategoryStore
from programy.storage.stores.nosql.mongo.store.learnf import MongoLearnfStore
from programy.storage.stores.nosql.mongo.store.errors import MongoErrorsStore
from programy.storage.stores.nosql.mongo.store.duplicates import MongoDuplicatesStore

from programy.storage.stores.nosql.mongo.store.conversations import MongoConversationStore
from programy.storage.stores.nosql.mongo.store.variables import MongoVariableStore

from programy.storage.stores.nosql.mongo.store.lookups import MongoDenormalStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoNormalStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoGenderStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoPersonStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoPerson2Store

from programy.storage.stores.nosql.mongo.store.properties import MongoPropertyStore
from programy.storage.stores.nosql.mongo.store.properties import MongoDefaultVariablesStore
from programy.storage.stores.nosql.mongo.store.properties import MongoRegexesStore

from programy.storage.stores.nosql.mongo.store.twitter import MongoTwitterStore

from programy.storage.stores.nosql.mongo.store.sets import MongoSetsStore
from programy.storage.stores.nosql.mongo.store.maps import MongoMapsStore
from programy.storage.stores.nosql.mongo.store.rdfs import MongoRDFsStore

from programy.storage.stores.nosql.mongo.store.spelling import MongoSpellingStore

from programy.storage.stores.nosql.mongo.store.licensekeys import MongoLicenseKeysStore

from programy.storage.stores.nosql.mongo.store.nodes import MongoPatternNodeStore
from programy.storage.stores.nosql.mongo.store.nodes import MongoTemplateNodeStore

from programy.storage.stores.nosql.mongo.store.processors import MongoPreProcessorStore
from programy.storage.stores.nosql.mongo.store.processors import MongoPostProcessorStore

from programy.storage.stores.nosql.mongo.store.usergroups import MongoUserGroupsStore

from programy.storage.stores.nosql.mongo.store.users import MongoUserStore
from programy.storage.stores.nosql.mongo.store.linkedaccounts import MongoLinkedAccountStore
from programy.storage.stores.nosql.mongo.store.links import MongoLinkStore


class MongoStorageEngine(StorageEngine):

    def __init__(self, configuration):
        StorageEngine.__init__(self, configuration)
        self._client = None
        self._database = None

    def initialise(self):
        self._client = MongoClient(self.configuration.url)

        if self.configuration.drop_all_first is True:
            self._client.drop_database(self.configuration.database)

        self._database = self._client.get_database(self.configuration.database)

        return True

    def category_store(self):
        return MongoCategoryStore(self)
    def learnf_store(self):
        return MongoLearnfStore(self)

    def errors_store(self):
        return MongoErrorsStore(self)
    def duplicates_store(self):
        return MongoDuplicatesStore(self)

    def conversation_store(self):
        return MongoConversationStore(self)

    def sets_store(self):
        return MongoSetsStore(self)
    def maps_store(self):
        return MongoMapsStore(self)
    def rdf_store(self):
        return MongoRDFsStore(self)

    def denormal_store(self):
        return MongoDenormalStore(self)
    def normal_store(self):
        return MongoNormalStore(self)
    def gender_store(self):
        return MongoGenderStore(self)
    def person_store(self):
        return MongoPersonStore(self)
    def person2_store(self):
        return MongoPerson2Store(self)

    def property_store(self):
        return MongoPropertyStore(self)
    def defaults_store(self):
        return MongoDefaultVariablesStore(self)
    def regex_store(self):
        return MongoRegexesStore(self)

    def variables_store(self):
        return MongoVariableStore(self)

    def twitter_store(self):
        return MongoTwitterStore(self)

    def spelling_store(self):
        return MongoSpellingStore(self)

    def license_store(self):
        return MongoLicenseKeysStore(self)

    def pattern_nodes_store(self):
        return MongoPatternNodeStore(self)
    def template_nodes_store(self):
        return MongoTemplateNodeStore(self)

    def preprocessors_store(self):
        return MongoPreProcessorStore(self)
    def postprocessors_store(self):
        return MongoPostProcessorStore(self)

    def usergroups_store(self):
        return MongoUserGroupsStore(self)

    def user_store(self):
        return MongoUserStore(self)
    def linked_account_store(self):
        return MongoLinkedAccountStore(self)
    def link_store(self):
        return MongoLinkStore(self)
