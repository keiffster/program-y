"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from programy.extensions.base import Extension


class AccountLinkingExtension(Extension):

    # LINK PRIMARY ACCOUNT $USERID $ACCOUNTNAME $GIVENTOKEN
    def handle_primary_account_link(self, context, words):
        if words[2] == 'ACCOUNT':
            if len(words) == 6:
                userid = words[3]
                account_name = words[4]
                given_token = words[5]
                return "PRIMARY ACCOUNT LINKED $GENERATEDTOKEN"

        return "INVALID PRIMARY ACCOUNT COMMAND"

    # LINK SECONDARY ACCOUNT $SECONDARY_USERID $SECONDARY_ACCOUNT_NAME $PRIMARY_USERID $PRIMARY_ACCOUNT_NAME $GIVEN_TOKEN $GENERATED_TOKEN
    def handle_secondary_account_link(self, context, words):
        if words[2] == 'ACCOUNT':
            if len(words) == 9:
                secondary_userid = words[3]
                secondary_account_name = words[4]
                primary_userid = words[5]
                primary_account_name = words[6]
                given_token = words[7]
                generated_token = words[8]
                return "SECONDARY ACCOUNT LINKED"

        return "INVALID SECONDARY ACCOUNT COMMAND"

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context, data):
        YLogger.debug(context, "Account Linking Extension - Calling external service for with extra data [%s]", data)

        words = data.split(" ")
        if words:
            if words[0] == 'LINK':
                if words[1] == 'PRIMARY':
                    return self.handle_primary_account_link(context, words)

                elif words[1] == 'SECONDARY':
                    return self.handle_secondary_account_link(context, words)

        return "ACCOUNT LINK FAILED UNKNOWN COMMAND"

