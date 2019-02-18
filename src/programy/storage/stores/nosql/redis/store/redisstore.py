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
from programy.storage.entities.store import Store

class RedisStore(Store):

    REDIS = "redis"

    def __init__(self, storage_engine):
        self._storage_engine = storage_engine

    def store_name(self):
        return RedisStore.REDIS

    @property
    def storage_engine(self):
        return self._storage_engine

    def commit(self):
        pass

    def delete(self, key):
        self._storage_engine._redis.delete(key)

    def save(self, h_key, s_key, clientid, properties):
        # Add clientid to sessions set
        pipeline = self._storage_engine._redis.pipeline()
        pipeline.sadd(s_key, clientid)

        # Save properties
        pipeline.hmset(h_key, properties)
        pipeline.execute()

    def is_member(self, s_key, clientid):
        # Check if clientid in sessions set
        return self._storage_engine._redis.sismember(s_key, clientid)

    def get(self, h_key):
        return self._storage_engine._redis.hgetall(h_key)

    def remove(self, s_key, clientid):
        self._storage_engine._redis.srem(s_key, clientid)

