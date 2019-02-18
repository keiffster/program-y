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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.linked import LinkedAccountStore
from programy.storage.stores.sql.dao.linked import LinkedAccount


class SQLLinkedAccountStore(SQLStore, LinkedAccountStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(LinkedAccount).delete()

    def link_accounts(self, primary_userid, linked_userid):
        shared = LinkedAccount(primary_user=primary_userid, linked_user=linked_userid)
        self._storage_engine.session.add(shared)
        return shared

    def unlink_accounts(self, primary_userid):
        try:
            self._storage_engine.session.query(LinkedAccount).filter(LinkedAccount.primary_user==primary_userid).delete()
            return True
        except Exception as e:
            return False

    def linked_accounts(self, primary_userid):
        db_accounts = self._storage_engine.session.query(LinkedAccount).filter(LinkedAccount.primary_user==primary_userid)
        accounts = []
        for account in db_accounts:
            accounts.append(account.linked_user)
        return accounts

    def primary_account(self, linked_userid):
        db_account = self._storage_engine.session.query(LinkedAccount).filter(LinkedAccount.linked_user==linked_userid).one()
        if db_account is not None:
            return db_account.primary_user
        return None