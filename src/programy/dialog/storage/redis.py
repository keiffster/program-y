"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import logging
import time

from programy.dialog.storage.base import ConversationStorage
import redis

class ConversationRedisStorage(ConversationStorage):

    def __init__(self, config):
        ConversationStorage.__init__(self, config)
        self._redis = redis.StrictRedis(
            host=config.host,
            port=config.port,
            password=config.password,
            db=0)

        self._prefix = config.prefix

        self._sessions_set_key = "{prefix}:sessions".format( prefix=self._prefix )

        # Make sure the client is able to connect to the redis instance
        assert self._redis.echo("test"), "Failed to connect to redis instance"

    def empty(self):

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Deleting Conversation redis data")

        redis = self._redis
        s_key = self._sessions_set_key

        try:
            redis.delete( s_key )

        except Exception as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed deleting conversation redis data")
                logging.exception(e)

    def save_conversation(self, conversation, clientid):

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Saving conversation to Redis for %s"%clientid)

        print("Writing to redis for %s"%clientid)

        redis = self._redis
        pipeline = redis.pipeline()

        clientid = str(clientid)
        s_key = self._sessions_set_key
        h_key = "{prefix}:{clientid}:props".format(
            prefix = self._prefix,
            clientid = clientid )

        props = conversation._properties

        try:
            # Add clientid to sessions set
            pipeline.sadd( s_key, clientid )

            # Save properties
            pipeline.hmset( h_key, props )
            pipeline.execute()

        except Exception as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed to save conversation to redis for clientid [%s]"%clientid)
                logging.exception(e)

    def load_conversation(self, conversation, clientid, restore_last_topic=False):

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Loading Conversation from file for %s"%clientid)

        print("Reading from redis for %s"%clientid)

        redis = self._redis

        clientid = str(clientid)
        s_key = self._sessions_set_key
        h_key = "{prefix}:{clientid}:props".format(
            prefix = self._prefix,
            clientid = clientid )

        conversation._properties = getattr(conversation, "_properties", {})

        try:
            # Check if clientid in sessions set
            convo_exists = redis.sismember( s_key, clientid )

            if not convo_exists:
                return

            # Fetch properties
            props = redis.hgetall( h_key )
            last_topic = props.pop("topic", None)

            # Update conversation
            conversation._properties.update(props)

            # Load last topic if required
            if restore_last_topic and last_topic:
                conversation._properties["topic"] = last_topic

        except Exception as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed to load conversation from redis for clientid [%s]"%clientid)
                logging.exception(e)

    def remove_conversation(self, clientid):

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Deleting Conversation redis data")

        redis = self._redis
        s_key = self._sessions_set_key
        clientid = str(clientid)

        try:
            redis.srem( s_key, clientid )

        except Exception as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed deleting conversation redis data for clientid [%s]"%clientid)
                logging.exception(e)
