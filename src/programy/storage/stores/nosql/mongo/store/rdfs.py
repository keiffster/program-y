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
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.rdf import RDFStore
from programy.storage.stores.nosql.mongo.dao.rdf import RDF

class MongoRDFsStore(MongoStore, RDFStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return 'rdfs'

    def empty_named(self, name):
        collection = self.collection()
        collection.remove({'name': name})

    def add_rdf(self, name, subject, predicate, objct):
        anrdf = RDF(name=name, subject=subject, predicate=predicate, object=objct)
        self.add_document(anrdf)

    def load_all(self, rdf_collection):
        collection = self.collection()
        rdfs = collection.find({})
        for rdf in rdfs:
            rdf_collection.add_entity(rdf['subject'], rdf['predicate'], rdf['object'], rdf['name'])

    def load(self, rdf_collection, rdf_name):
        collection = self.collection()
        rdfs = collection.find({'name': rdf_name})
        for rdf in rdfs:
            rdf_collection.add_entity(rdf['subject'], rdf['predicate'], rdf['object'], rdf_name)


