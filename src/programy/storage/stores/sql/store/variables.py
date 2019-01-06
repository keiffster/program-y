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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.variables import VariablesStore
from programy.storage.stores.sql.dao.variables import Variable

class SQLVariablesStore(SQLStore, VariablesStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(Variable).delete()

    def empty_variables(self, clientid, userid):
        self._storage_engine.session.query(Variable).filter(Variable.clientid==clientid, Variable.userid==userid).delete()

    def add_variable(self, clientid, userid, name, value):
        var = Variable(clientid=clientid, userid=userid, name=name, value=value)
        self._storage_engine.session.add(var)

    def add_variables(self, clientid, userid, variables):
        for name, value in variables.items():
            var = Variable(clientid=clientid, userid=userid, name=name, value=value)
            self._storage_engine.session.add(var)

    def get_variables(self, clientid, userid):
        db_vars = self._storage_engine.session.query(Variable).filter(Variable.clientid==clientid, Variable.userid==userid)
        vars = {}
        for var in db_vars:
            vars[var.name] = var.value
        return vars

    def get_storage(self):
        return self.storage_engine.configuration.variables_storage

