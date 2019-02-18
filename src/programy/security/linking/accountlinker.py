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
import string
import random
import datetime

"""
Workflow is 

1. User is associated with an initial PRIMARY Client, e.g Facebook


2. User decides to link account and ask PY to initiate an action

3. PY asks them to login into primary account and ask for a LINK TOKEN
    As part of the process they are asked to provide a SECRET they know
    PY then provides a LINK TOKEN
    User now has
                PRIMARY ACCOUNT ID
                PRIMARY ACCOUNT NAME
                GIVEN TOKEN
                GENERATED TOKEN

        -> LINK PRIMARY ACCOUNT $USERID $ACCOUNTNAME $GIVENTOKEN

        <- PRIMARY ACCOUNT LINKED $GENERATEDTOKEN
        <-> PRIMARY ACCOUNT LINK FAILED $REASON

    Link has a expirary time, circa 1 hr, after which link expires and now tokens will need to be requested

4. PY now tells them to log into the client they want to link

5. User logs into secondary account and asks to link this to primary account

6. PY Asks for 
                PRIMARY ACCOUNT ID
                PRIMARY ACCOUNT NAME
                GIVEN TOKEN
                GENERATED TOKEN

        -> LINK SECONDARY ACCOUNT $SECONDARY_USERID $SECONDARY_ACCOUNT_NAME $PRIMARY_USERID $PRIMARY_ACCOUNT_NAME $GIVEN_TOKEN $GENERATED_TOKEN
        
        <- SECONDARY ACCOUNT LINKED
        <- SECONDARY ACCOUNT LINK FAILED $REASON

7. PY Links accounts
"""


class BasicAccountLinkerService(object):

    KEY_CHARS = string.ascii_uppercase + string.digits
    TWENTY_FOUR_HOURS = 24 * 60 * 60
    MAX_RETRIES = 3

    def __init__(self, storage_engine):
        self._storage_engine = storage_engine

    def initialise(self, client):
        pass

    def link_user_to_client(self, userid, clientid):

        assert (userid is not None)
        assert (clientid is not None)

        if self._storage_engine.user_store().exists(userid, clientid) is True:
            return True

        if self._storage_engine.user_store().add_user(userid, clientid) is not None:
            return True

        return False

    def linked_accounts(self, userid):

        assert (userid is not None)

        return self._storage_engine.user_store().get_links(userid)

    def unlink_user_from_client(self, userid, clientid):

        assert (userid is not None)
        assert (clientid is not None)

        if self._storage_engine.user_store().remove_user(userid, clientid) is True:
            if self._storage_engine.link_store().remove_link(userid) is True:
                if self._storage_engine.linked_account_store().unlink_accounts(userid) is True:
                    return True

        return False

    def unlink_user_from_all_clients(self, userid):

        assert (userid is not None)

        if self._storage_engine.user_store().remove_user_from_all_clients(userid) is True:
            if self._storage_engine.link_store().remove_link(userid) is True:
                if self._storage_engine.linked_account_store().unlink_accounts(userid) is True:
                    return True

        return False

    def _generate_key(self, size=8):
        return ''.join(random.choice(BasicAccountLinkerService.KEY_CHARS) for _ in range(size))

    def _generate_expirary(self, lifetime):
        return datetime.datetime.now() + datetime.timedelta(seconds=lifetime)

    def generate_link(self, userid, provided_key, lifetime=TWENTY_FOUR_HOURS):

        assert (userid is not None)
        assert (provided_key is not None)

        generated_key = self._generate_key()
        expires = self._generate_expirary(lifetime)

        if self._storage_engine.link_store().create_link(userid, provided_key, generated_key, expires) is not None:
            return generated_key

        return None

    def _has_link_expired(self, link):

        assert (link is not None)

        now = datetime.datetime.now()
        if now > link.expires:
            return True

        return False

    def _expire_link(self, link):

        assert (link is not None)

        link.expired = True
        self._storage_engine.link_store().update_link(link)

    def _valid_link_keys(self, link, provided_key, generated_key, max_retries):

        assert (link is not None)

        if link.generated_key == generated_key:
            if link.provided_key == provided_key:
               if link.retry_count < max_retries:
                   return True

        return False

    def _inc_retry_count(self, link):

        assert (link is not None)

        link.retry_count += 1
        self._storage_engine.link_store().update_link(link)

    def link_accounts(self, userid, provided_key, generated_key, linked_userid, linked_client):

        assert (userid is not None)
        assert (provided_key is not None)
        assert (generated_key is not None)
        assert (linked_userid is not None)
        assert (linked_client is not None)

        link = self._storage_engine.link_store().get_link(userid)
        if link is not None:

            if link.expired is False:

                if self._has_link_expired(link) is True:
                    self._expire_link(link)

                elif self._valid_link_keys(link, provided_key, generated_key, BasicAccountLinkerService.MAX_RETRIES) is False:
                    self._inc_retry_count(link)

                elif self._storage_engine.user_store().add_user(linked_userid, linked_client) is not None:

                    if self._storage_engine.linked_account_store().link_accounts(userid, linked_userid) is not None:
                        return True

        return False

    def reset_link(self, userid):

        assert (userid is not None)

        link = self._storage_engine.link_store().get_link(userid)

        if link is not None:
            link.retry_count = 0
            self._storage_engine.link_store().update_link(link)
            return True

        return False

    def primary_account(self, secondary_userid):

        assert (secondary_userid is not None)

        return self._storage_engine.linked_account_store().primary_account(secondary_userid)

