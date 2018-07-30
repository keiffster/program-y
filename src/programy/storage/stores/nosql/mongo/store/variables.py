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
from programy.storage.entities.variables import VariablesStore
from programy.storage.stores.nosql.mongo.dao.variable import Variables


class MongoVariableStore(MongoStore, VariablesStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return 'variables'

    def empty_variables(self, clientid, userid):
        collection = self.collection()
        collection.remove({'clientid': clientid, 'userid': userid})

    def add_variable(self, clientid, userid, name, value):
        collection = self.collection()
        variables = collection.find_one({"clientid": clientid, "userid": userid})
        if variables is not None:
            variables['variables'][name] = value
            collection.update({"clientid": clientid, "userid": userid}, variables)
        else:
            variables = Variables(clientid, userid)
            variables.variables[name] = value
            self.add_document(variables)
        return variables

    def add_variables(self, clientid, userid, variables):
        collection = self.collection()
        document = collection.find_one({"clientid": clientid, "userid": userid})
        if document is not None:
            props = Variables(clientid, userid)
            for key, value in variables.items():
                props.variables[key] = value
            self.replace_document(props)
        else:
            props = Variables(clientid, userid)
            for key, value in variables.items():
                props.variables[key] = value
            self.add_document(props)

    def get_variables(self, clientid, userid):
        collection = self.collection()
        variables = collection.find_one({"clientid": clientid, "userid": userid})
        if variables is not None:
            return variables['variables']
        return {}
