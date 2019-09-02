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

import json

from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.entities.conversation import ConversationStore


class RedisConversationStore(RedisStore, ConversationStore):

    CHUNK_SIZE = 5000

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def _create_key(self, client_context):
        return "{prefix}:conversation:{clientid}".format(prefix=self._storage_engine.prefix,
                                                         clientid=client_context.client.id)

    def _create_ns_keys(self):
        return "{prefix}:*".format(prefix=self._storage_engine.prefix)

    def empty(self):
        ns_keys = self._create_ns_keys()

        YLogger.info(self, "Emptying Conversation from Redis [%s]", ns_keys)

        cursor = '0'
        while cursor != 0:
            cursor, keys = self._storage_engine._redis.scan(cursor=cursor, match=ns_keys, count=RedisConversationStore.CHUNK_SIZE)
            if keys:
                self._storage_engine._redis.delete(*keys)

    def store_conversation(self, client_context, conversation):
        try:
            convo_key = self._create_key(client_context)
            YLogger.debug(self, "Adding conversation [%s]", convo_key)

            json_convo = conversation.to_json()
            json_str = json.dumps(json_convo)

            self.save(convo_key, json_str)

        except Exception as e:
            YLogger.exception (self, "Failed to save conversation to Redis for clientid [%s]", e, client_context.client.id)

    def load_conversation(self, client_context, conversation):

        try:
            h_key = self._create_key(client_context)
            s_key = self._storage_engine.sessions_set_key

            YLogger.debug(self, "Loading Conversation from cache  %s %s", h_key, s_key)

            # Fetch conversation
            YLogger.debug(self, "Fetching conversation [%s]", h_key)
            json_str = self.get(h_key)
            json_convo = json.loads(json_str)

            conversation.create_from_json(json_convo)

        except Exception as e:
            YLogger.exception(self, "Failed to load conversation from Redis for clientid [%s]",e, client_context.client.id)

        return conversation

