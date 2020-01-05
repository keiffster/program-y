"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.rdf import RDFReadWriteStore
from programy.storage.stores.sql.dao.rdf import RDF
from programy.utils.console.console import outputLog


class SQLRDFsStore(RDFReadWriteStore, SQLStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        RDFReadWriteStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(RDF)

    def empty(self):
        self._get_all().delete()

    def empty_named(self, name):
        self._storage_engine.session.query(RDF).filter(RDF.name == name).delete()

    def add_rdf(self, name, subject, predicate, objct, replace_existing=True):
        del replace_existing
        anrdf = RDF(name=name, subject=subject, predicate=predicate, object=objct)
        self._storage_engine.session.add(anrdf)
        return True

    def load_all(self, collector):
        names = self._storage_engine.session.query(RDF.name).distinct()
        for name in names:
            self.load(collector, name[0])

    def load(self, collector, name=None):
        db_rdfs = self._storage_engine.session.query(RDF).filter(RDF.name == name)
        for rdf in db_rdfs:
            collector.add_entity(rdf.subject, rdf.predicate, rdf.object, name)

