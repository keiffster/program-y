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
import string
import random


class LinkedAccountsManager(object):

    KEY_CHARS = string.ascii_uppercase + string.digits

    def __init__(self, storage_engine):
        self._storage_engine = storage_engine

    def link_user_to_client(self, userid, clientid):

        assert (userid is not None)
        assert (clientid is not None)

        if self._storage_engine.user_store.add_user(userid, clientid) is not None:
            return True

        return False

    def unlink_user_from_client(self, userid, clientid):

        assert (userid is not None)
        assert (clientid is not None)

    def unlink_user_from_all_clients(self, userid):

        assert (userid is not None)

    def generate_link(self, userid, provided_key):

        assert (userid is not None)
        assert (provided_key is not None)

        generated_key = self._generate_key()

        if self._storage_engine.link_store.create_link(self, userid, generated_key, provided_key) is not None:
            return generated_key

        return None

    def _generate_key(self, size=8):
        return ''.join(random.choice(LinkedAccountsManager.KEY_CHARS) for _ in range(size))