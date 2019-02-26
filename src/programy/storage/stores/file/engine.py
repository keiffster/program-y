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

from programy.storage.engine import StorageEngine
from programy.storage.stores.file.store.properties import FilePropertyStore
from programy.storage.stores.file.store.properties import FileDefaultVariablesStore
from programy.storage.stores.file.store.conversations import FileConversationStore
from programy.storage.stores.file.store.twitter import FileTwitterStore
from programy.storage.stores.file.store.sets import FileSetsStore
from programy.storage.stores.file.store.maps import FileMapsStore
from programy.storage.stores.file.store.rdfs import FileRDFStore
from programy.storage.stores.file.store.lookups import FileDenormalStore
from programy.storage.stores.file.store.lookups import FileNormalStore
from programy.storage.stores.file.store.lookups import FileGenderStore
from programy.storage.stores.file.store.lookups import FilePersonStore
from programy.storage.stores.file.store.lookups import FilePerson2Store
from programy.storage.stores.file.store.properties import FileRegexStore
from programy.storage.stores.file.store.errors import FileErrorsStore
from programy.storage.stores.file.store.duplicates import FileDuplicatesStore
from programy.storage.stores.file.store.categories import FileCategoryStore
from programy.storage.stores.file.store.learnf import FileLearnfStore
from programy.storage.stores.file.store.variables import FileVariablesStore
from programy.storage.stores.file.store.spelling import FileSpellingStore
from programy.storage.stores.file.store.licensekeys import FileLicenseStore
from programy.storage.stores.file.store.nodes import FilePatternNodeStore
from programy.storage.stores.file.store.nodes import FileTemplateNodeStore
from programy.storage.stores.file.store.binaries import FileBinariesStore
from programy.storage.stores.file.store.braintree import FileBraintreeStore
from programy.storage.stores.file.store.processors import FilePreProcessorsStore
from programy.storage.stores.file.store.processors import FilePostProcessorsStore
from programy.storage.stores.file.store.usergroups import FileUserGroupStore
from programy.storage.stores.file.store.triggers import FileTriggersStore


class FileStorageEngine(StorageEngine):

    FILE = "file"

    def __init__(self, configuration):
        StorageEngine.__init__(self, configuration)

    def initialise(self):
        return True

    def category_store(self):
        return FileCategoryStore(self)
    def errors_store(self):
        return FileErrorsStore(self)
    def duplicates_store(self):
        return FileDuplicatesStore(self)
    def learnf_store(self):
        return FileLearnfStore(self)

    def conversation_store(self):
        return FileConversationStore(self)

    def sets_store(self):
        return FileSetsStore(self)
    def maps_store(self):
        return FileMapsStore(self)
    def rdf_store(self):
        return FileRDFStore(self)

    def denormal_store(self):
        return FileDenormalStore(self)
    def normal_store(self):
        return FileNormalStore(self)
    def gender_store(self):
        return FileGenderStore(self)
    def person_store(self):
        return FilePersonStore(self)
    def person2_store(self):
        return FilePerson2Store(self)
    def regex_store(self):
        return FileRegexStore(self)

    def property_store(self):
        return FilePropertyStore(self)
    def defaults_store(self):
        return FileDefaultVariablesStore(self)
    def variables_store(self):
        return FileVariablesStore(self)

    def twitter_store(self):
        return FileTwitterStore(self)

    def spelling_store(self):
        return FileSpellingStore(self)

    def license_store(self):
        return FileLicenseStore(self)

    def pattern_nodes_store(self):
        return FilePatternNodeStore(self)
    def template_nodes_store(self):
        return FileTemplateNodeStore(self)

    def binaries_store(self):
        return FileBinariesStore(self)

    def braintree_store(self):
        return FileBraintreeStore(self)

    def preprocessors_store(self):
        return FilePreProcessorsStore(self)
    def postprocessors_store(self):
        return FilePostProcessorsStore(self)

    def usergroups_store(self):
        return FileUserGroupStore(self)

    def triggers_store(self):
        return FileTriggersStore(self)