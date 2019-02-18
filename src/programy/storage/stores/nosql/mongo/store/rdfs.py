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
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.rdf import RDFStore
from programy.storage.stores.nosql.mongo.dao.rdf import RDF

class MongoRDFsStore(MongoStore, RDFStore):

    RDFS = 'rdfs'
    SUBJECT = 'subject'
    PREDICATE = 'predicate'
    OBJECT = 'object'
    NAME = 'name'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoRDFsStore.RDFS

    def empty_named(self, name):
        YLogger.info(self, "Empting rdf [%s]", name)
        collection = self.collection()
        collection.remove({MongoRDFsStore.NAME: name})

    def add_rdf(self, name, subject, predicate, objct, replace_existing=True):
        collection = self.collection()
        YLogger.info(self, "Adding RDF [%s] [%s] [%s] [%s]", name, subject, predicate, objct)
        anrdf = RDF(name=name, subject=subject, predicate=predicate, object=objct)
        collection.insert_one(anrdf.to_document())
        return True

    def load_all(self, rdf_collection):
        YLogger.info(self, "Loading all RDFs")
        collection = self.collection()
        rdfs = collection.find({})
        for rdf in rdfs:
            YLogger.info(self, "Loading RDF [%s]", rdf[MongoRDFsStore.NAME])
            rdf_collection.add_entity(rdf[MongoRDFsStore.SUBJECT], rdf[MongoRDFsStore.PREDICATE], rdf[MongoRDFsStore.OBJECT], rdf[MongoRDFsStore.NAME])

    def load(self, rdf_collection, rdf_name):
        collection = self.collection()
        rdfs = collection.find({MongoRDFsStore.NAME: rdf_name})
        for rdf in rdfs:
            YLogger.info(self, "Loading RDF [%s]", rdf[MongoRDFsStore.NAME])
            rdf_collection.add_entity(rdf[MongoRDFsStore.SUBJECT], rdf[MongoRDFsStore.PREDICATE], rdf[MongoRDFsStore.OBJECT], rdf_name)


