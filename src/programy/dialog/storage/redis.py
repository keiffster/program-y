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
import redis

from programy.dialog.storage.base import ConversationStorage
from programy.utils.logging.ylogger import YLogger

class RedisStorage(object):

    def __init__(self, config):
        self._redis = redis.StrictRedis(
            host=config.host,
            port=config.port,
            password=config.password,
            db=0)

    def delete(self, key):
        self._redis.delete(key)

    def save(self, h_key,s_key, clientid, properties):
        # Add clientid to sessions set
        pipeline = self._redis.pipeline()
        pipeline.sadd(s_key, clientid)

        # Save properties
        pipeline.hmset(h_key, properties)
        pipeline.execute()

    def is_member(self, s_key, clientid):
        # Check if clientid in sessions set
        return self._redis.sismember(s_key, clientid)

    def get(self, h_key):
        return self._redis.hgetall(h_key)

    def remove(self, s_key, clientid):
        self._redis.srem(s_key, clientid)


class RedisFactory(object):

    @staticmethod
    def connect(config):
        return RedisStorage(config)


class ConversationRedisStorage(ConversationStorage):

    def __init__(self, config, factory=None):
        ConversationStorage.__init__(self, config)
        if factory is None:
            self._redis = RedisFactory.connect(config)
        else:
            self._redis = factory.connect(config)

        self._prefix = config.prefix
        self._sessions_set_key = "{prefix}:sessions".format( prefix=self._prefix )

        # Make sure the client is able to connect to the redis instance
        #assert self._redis.echo("test"), "Failed to connect to redis instance"

    def empty(self):

        YLogger.debug(self, "Deleting Conversation redis data")

        try:
            self._redis.delete(self._sessions_set_key)

        except Exception as e:
            YLogger.exception(self, "Failed deleting conversation redis data", e)

    def save_conversation(self, conversation, clientid):

        YLogger.debug(self, "Saving conversation to Redis for %s"%clientid)

        h_key = "{prefix}:{clientid}:props".format(
            prefix = self._prefix,
            clientid = clientid )

        try:
            self._redis.save(h_key, self._sessions_set_key, clientid, conversation._properties)

        except Exception as e:
            YLogger.exception(self, "Failed to save conversation to redis for clientid [%s]"%clientid, e)

    def load_conversation(self, conversation, clientid, restore_last_topic=False):

        YLogger.debug(self, "Loading Conversation from file for %s"%clientid)

        h_key = "{prefix}:{clientid}:props".format(prefix = self._prefix, clientid = clientid)

        try:
            # Check if clientid in sessions set
            if not self._redis.is_member( self._sessions_set_key, clientid ):
                return

            # Fetch properties
            props = self._redis.get(h_key)
            last_topic = props["topic"]

            # Update conversation
            conversation._properties.update(props)

            # Load last topic if required
            if restore_last_topic and last_topic:
                conversation._properties["topic"] = last_topic

        except Exception as e:
            YLogger.exception(self, "Failed to load conversation from redis for clientid [%s]"%clientid, e)

    def remove_conversation(self, clientid):

        YLogger.debug("Deleting Conversation redis data")

        try:
            self._redis.remove(self._sessions_set_key, clientid)

        except Exception as e:
            YLogger.exception(self, "Failed deleting conversation redis data for clientid [%s]"%clientid, e)
