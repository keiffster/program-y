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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from programy.storage.engine import StorageEngine
from programy.storage.stores.sql.base import Base

from programy.storage.stores.sql.store.users import SQLUserStore
from programy.storage.stores.sql.store.linkedaccounts import SQLLinkedAccountStore
from programy.storage.stores.sql.store.links import SQLLinkStore

from programy.storage.stores.sql.store.properties import SQLPropertyStore
from programy.storage.stores.sql.store.properties import SQLRegexStore
from programy.storage.stores.sql.store.properties import SQLDefaultVariableStore

from programy.storage.stores.sql.store.variables import SQLVariablesStore

from programy.storage.stores.sql.store.categories import SQLCategoryStore
from programy.storage.stores.sql.store.learnf import SQLLearnfStore
from programy.storage.stores.sql.store.conversations import SQLConversationStore

from programy.storage.stores.sql.store.sets import SQLSetsStore
from programy.storage.stores.sql.store.maps import SQLMapsStore
from programy.storage.stores.sql.store.rdfs import SQLRDFsStore

from programy.storage.stores.sql.store.lookups import SQLDenormalStore
from programy.storage.stores.sql.store.lookups import SQLNormalStore
from programy.storage.stores.sql.store.lookups import SQLGenderStore
from programy.storage.stores.sql.store.lookups import SQLPersonStore
from programy.storage.stores.sql.store.lookups import SQLPerson2Store
from programy.storage.stores.sql.store.errors import SQLErrorsStore

from programy.storage.stores.sql.store.duplicates import SQLDuplicatesStore

from programy.storage.stores.sql.store.twitter import SQLTwitterStore

from programy.storage.stores.sql.store.spelling import SQLSpellingStore

from programy.storage.stores.sql.store.licensekeys import SQLLicenseKeysStore

from programy.storage.stores.sql.store.nodes import SQLPatternNodesStore
from programy.storage.stores.sql.store.nodes import SQLTemplateNodesStore

from programy.storage.stores.sql.store.processors import SQLPreProcessorsStore
from programy.storage.stores.sql.store.processors import SQLPostProcessorsStore

from programy.storage.stores.sql.store.usergroups import SQLUserGroupStore


class SQLStorageEngine(StorageEngine):

    def __init__(self, configuration):
        StorageEngine.__init__(self, configuration)
        self._session = None

    def initialise(self):
        self._engine = create_engine(self.configuration.url, encoding=self.configuration.encoding, echo=self.configuration.echo)

        if self.configuration.drop_all_first is True:
            Base.metadata.drop_all(self._engine)

        if self.configuration.create_db is True:
            Base.metadata.create_all(self._engine)

        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        return True

    @property
    def session(self):
        return self._session

    def user_store(self):
        return SQLUserStore(self)
    def linked_account_store(self):
        return SQLLinkedAccountStore(self)
    def link_store(self):
        return SQLLinkStore(self)

    def category_store(self):
        return SQLCategoryStore(self)
    def errors_store(self):
        return SQLErrorsStore(self)
    def duplicates_store(self):
        return SQLDuplicatesStore(self)
    def learnf_store(self):
         return SQLLearnfStore(self)

    def conversation_store(self):
        return SQLConversationStore(self)

    def sets_store(self):
        return SQLSetsStore(self)
    def maps_store(self):
        return SQLMapsStore(self)
    def rdf_store(self):
        return SQLRDFsStore(self)

    def denormal_store(self):
        return SQLDenormalStore(self)
    def normal_store(self):
        return SQLNormalStore(self)
    def gender_store(self):
        return SQLGenderStore(self)
    def person_store(self):
        return SQLPersonStore(self)
    def person2_store(self):
        return SQLPerson2Store(self)
    def regex_store(self):
        return SQLRegexStore(self)

    def property_store(self):
        return SQLPropertyStore(self)
    def defaults_store(self):
        return SQLDefaultVariableStore(self)
    def variables_store(self):
        return SQLVariablesStore(self)

    def twitter_store(self):
        return SQLTwitterStore(self)

    def spelling_store(self):
        return SQLSpellingStore(self)

    def license_store(self):
        return SQLLicenseKeysStore(self)

    def pattern_nodes_store(self):
        return SQLPatternNodesStore(self)
    def template_nodes_store(self):
        return SQLTemplateNodesStore(self)

    def preprocessors_store(self):
        return SQLPreProcessorsStore(self)
    def postprocessors_store(self):
        return SQLPostProcessorsStore(self)

    def usergroups_store(self):
        return SQLUserGroupStore(self)

