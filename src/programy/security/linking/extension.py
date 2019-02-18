"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This is an example extension that allow syou to call an external service to retreive the bank balance
of the customer. Currently contains no authentication
"""
from programy.utils.logging.ylogger import YLogger

from programy.context import ClientContext
from programy.extensions.base import Extension
from programy.security.linking.accountlinker import BasicAccountLinkerService

class AccountLinkingExtension(Extension):

    def get_account_linker_service(self, context: ClientContext) -> BasicAccountLinkerService:

        assert (isinstance(context, ClientContext))

        return context.brain.security.account_linker

    # LINK PRIMARY ACCOUNT $USERID $ACCOUNTNAME $GIVENTOKEN
    def handle_primary_account_link(self, context: ClientContext, words: list):

        assert (isinstance(context, ClientContext))
        assert (isinstance(words, list))

        if words[2] == 'ACCOUNT':
            if len(words) == 6:
                userid = words[3]
                account_name = words[4]
                provided_key = words[5]

                linked = self.get_account_linker_service(context)

                assert (isinstance(linked, BasicAccountLinkerService))

                if linked is not None:
                    generated_key = linked.generate_link( userid, provided_key)
                    if generated_key is not None:
                        if linked.link_user_to_client(userid, account_name) is True:
                            return "PRIMARY ACCOUNT LINKED %s"%generated_key

        return "INVALID PRIMARY ACCOUNT COMMAND"

    # LINK SECONDARY ACCOUNT $SECONDARY_USERID $SECONDARY_ACCOUNT_NAME $PRIMARY_USERID $GIVEN_TOKEN $GENERATED_TOKEN
    def handle_secondary_account_link(self, context: ClientContext, words: list) -> str:

        assert (isinstance(context, ClientContext))
        assert (isinstance(words, list))

        if words[2] == 'ACCOUNT':
            if len(words) == 8:
                primary_userid = words[3]
                secondary_userid = words[4]
                secondary_account_name = words[5]
                provided_key = words[6]
                generated_key = words[7]

                linked = self.get_account_linker_service(context)

                assert (isinstance(linked, BasicAccountLinkerService))

                if linked is not None:
                    if linked.link_accounts(primary_userid, provided_key, generated_key, secondary_userid, secondary_account_name) is True:
                        return "SECONDARY ACCOUNT LINKED"

        return "INVALID SECONDARY ACCOUNT COMMAND"

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context: ClientContext, data: str) -> str:

        assert (isinstance(context, ClientContext))
        assert (isinstance(data, str))

        YLogger.debug(context, "Account Linking Extension - Calling external service for with extra data [%s]", data)

        words = data.split(" ")
        if words:
            if words[0] == 'LINK':
                if words[1] == 'PRIMARY':
                    return self.handle_primary_account_link(context, words)

                elif words[1] == 'SECONDARY':
                    return self.handle_secondary_account_link(context, words)

        return "ACCOUNT LINK FAILED UNKNOWN COMMAND"

