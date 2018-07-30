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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.link import LinkStore
from programy.storage.stores.sql.dao.link import Link


class SQLLinkStore(SQLStore, LinkStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(Link).delete()

    def create_link(self, primary_userid, generated_key, provided_key):
        link = Link(primary_user=primary_userid, generated_key=generated_key, provided_key=provided_key)
        self._storage_engine.session.add(link)
        return link

    def get_link(self, primary_userid):
        db_links = self._storage_engine.session.query(Link).filter(Link.primary_user==primary_userid)
        links = []
        for link in db_links:
            links.append({"primary_user": link.primary_user, "generated_key": link.generated_key, "provided_key": link.provided_key})
        return links

    def remove_link(self, primary_userid):
        self._storage_engine.session.query(Link).filter(Link.primary_user==primary_userid).delete()
