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
from programy.storage.entities.variables import VariablesStore
from programy.storage.stores.nosql.mongo.dao.variable import Variables


class MongoVariableStore(MongoStore, VariablesStore):

    VARIABLES = 'variables'
    CLIENTID = 'clientid'
    USERID = 'userid'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoVariableStore.VARIABLES

    def empty_variables(self, clientid, userid):
        YLogger.info(self, "Emptying variables for clientid [%s], userid [%s]", clientid, userid)
        collection = self.collection()
        collection.delete_many({MongoVariableStore.CLIENTID: clientid, MongoVariableStore.USERID: userid})

    def add_variable(self, clientid, userid, name, value, replace_existing=True):
        collection = self.collection()
        variables = collection.find_one({MongoVariableStore.CLIENTID: clientid, "userid": userid})
        if variables is not None:
            if replace_existing is True:
                YLogger.debug(self, "Replacing existing variable [%s=%s] for clientid [%s], userid [%s]", name, value, clientid,userid)
                variables[MongoVariableStore.VARIABLES][name] = value
                collection.replace_one({MongoVariableStore.CLIENTID: clientid, "userid": userid}, variables)
            else:
                YLogger.debug(self, "Variable already exists [%s=%s] for clientid [%s], userid [%s]", name, value, clientid,userid)
                return False
        else:
            YLogger.debug(self, "Adding variable [%s=%s] for clientid [%s], userid [%s]", name, value, clientid, userid)
            variables = Variables(clientid, userid, {})
            variables.variables[name] = value
            self.add_document(variables)
        return True

    def add_variables(self, clientid, userid, variables, replace_existing=True):
        collection = self.collection()
        document = collection.find_one({MongoVariableStore.CLIENTID: clientid, MongoVariableStore.USERID: userid})
        if document is not None:
            if replace_existing is True:
                YLogger.debug(self, "Replacing existing variables for clientid [%s], userid [%s]", clientid, userid)
                props = Variables(clientid, userid)
                for key, value in variables.items():
                    props.variables[key] = value
                self.replace_document(props)
            else:
                YLogger.debug(self, "Variablse already exist for clientid [%s], userid [%s]", clientid, userid)
                return False
        else:
            YLogger.debug(self, "Adding variables for clientid [%s], userid [%s]", clientid, userid)
            props = Variables(clientid, userid, {})
            for key, value in variables.items():
                props.variables[key] = value
            self.add_document(props)
        return True

    def get_variables(self, clientid, userid):
        collection = self.collection()
        variables = collection.find_one({MongoVariableStore.CLIENTID: clientid, MongoVariableStore.USERID: userid})
        if variables is not None:
            return variables[MongoVariableStore.VARIABLES]
        return {}
