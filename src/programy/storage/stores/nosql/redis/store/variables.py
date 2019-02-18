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

from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.entities.variables import VariablesStore

class RedisVariableStore(RedisStore, VariablesStore):

    CHUNK_SIZE = 5000

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def create_key(self, clientid, userid):
        return "{prefix}:{clientid}{userid}:props".format(prefix=self._storage_engine._prefix, clientid=clientid, userid=userid )

    def empty(self):
        ns_keys = "programy:*"

        YLogger.info(self, "Emptying Conversation from Redis [%s]", ns_keys)

        cursor = '0'
        while cursor != 0:
            cursor, keys = self._storage_engine._redis.scan(cursor=cursor, match=ns_keys, count=RedisVariableStore.CHUNK_SIZE)
            if keys:
                self._storage_engine._redis.delete(*keys)

    def add_variable(self, clientid, userid, name, value):
        YLogger.info(self, "Adding variable to Redis [%s] [%s] [%s] [%s]", clientid, userid, name, value)

        variables = self.get_variables(clientid, userid)
        if variables:
            variables[name] = value
        else:
            variables = {name: value}

        self.add_variables(clientid, userid, variables)

    def add_variables(self, clientid, userid, variables):
        YLogger.info(self, "Adding variables to Redis [%s] [%s] [%s]", clientid, userid, variables)
        try:
            h_key = self.create_key(clientid, userid)
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Adding variables [%s] - [%s]", s_key, h_key)
            self.save(h_key, s_key, clientid, variables)

        except Exception as e:
            YLogger.exception (self, "Failed to save conversation to Redis for clientid [%s]", e, clientid)

    def get_variables(self, clientid, userid, restore_last_topic=False):

        YLogger.debug(self, "Loading Conversation from cache for %s", clientid)

        try:
            h_key = self.create_key(clientid, userid)
            s_key = self._storage_engine._sessions_set_key

            # Check if clientid in sessions set
            if not self.is_member(s_key, clientid ):
                YLogger.debug(self, "Clientid [%s], not in sessions [%s]", clientid, s_key)
                return {}

            # Fetch variables
            YLogger.debug(self, "Fetching variables [%s]", h_key)
            props = self.get(h_key)

            variables = {}
            for key, value in props.items():
                variables[key.decode('utf-8')] = value.decode('utf-8')

            if restore_last_topic is True:
                if "topic" in variables:
                    last_topic = variables["topic"]
                    # Load last topic if required
                    if last_topic:
                        variables["topic"] = last_topic

            return variables

        except Exception as e:
            YLogger.exception(self, "Failed to load conversation from Redis for clientid [%s]",e, clientid)

        return {}

    def empty_variables(self, clientid, userid):

        ns_keys = self.create_key(clientid, userid)

        YLogger.debug(self, "Emptying Conversation from Redis [%s]", ns_keys)

        cursor = '0'
        while cursor != 0:
            cursor, keys = self._storage_engine._redis.scan(cursor=cursor, match=ns_keys, count=RedisVariableStore.CHUNK_SIZE)
            if keys:
                self._storage_engine._redis.delete(*keys)

