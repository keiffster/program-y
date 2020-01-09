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
from programy.storage.entities.store import Store


class RedisStore(Store):

    def __init__(self, storage_engine):
        Store.__init__(self)
        self._storage_engine = storage_engine

    @property
    def storage_engine(self):
        return self._storage_engine

    def commit(self, commit=True):
        del commit
        pass    # pragma: no cover

    def delete(self, key):
        self._storage_engine.redis.delete(key)

    def save(self, convo_key, conversation_str):
        # Add clientid to sessions set
        pipeline = self._storage_engine.redis.pipeline()

        # Save properties
        pipeline.set(convo_key, conversation_str)
        pipeline.execute()

    def get(self, h_key):
        result = self._storage_engine.redis.get(h_key)
        if result is not None:
            return result.decode("utf-8")
        return result