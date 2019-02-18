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
from programy.utils.logging.ylogger import YLogger
from programy.utils.classes.loader import ClassLoader
from programy.dialog.sentence import Sentence
from programy.config.brain.securities import BrainSecuritiesConfiguration


class SecurityManager(object):

    def __init__(self, security_configuration):

        assert (security_configuration is not None)
        assert (isinstance(security_configuration, BrainSecuritiesConfiguration))

        self._configuration = security_configuration
        self._authentication = None
        self._authorisation = None
        self._account_linker = None

    @property
    def authentication(self):
        return self._authentication

    @property
    def authorisation(self):
        return self._authorisation

    @property
    def account_linker(self):
        return self._account_linker

    def load_security_services(self, client):
        if self._configuration is not None:
            self.load_authentication_service(client)
            self.load_authorisation_service(client)
            self.load_account_linking_service(client)
        else:
            YLogger.debug(self, "No security configuration defined, running open...")

    def load_authentication_service(self, client):
        if self._configuration.authentication is not None:
            if self._configuration.authentication.classname is not None:
                try:
                    classobject = ClassLoader.instantiate_class(self._configuration.authentication.classname)
                    self._authentication = classobject(self._configuration.authentication)
                    self._authentication.initialise(client)
                except Exception as excep:
                    YLogger.exception(self, "Failed to load security services", excep)
        else:
            YLogger.debug(self, "No authentication configuration defined")

    def load_authorisation_service(self, client):
        if self._configuration.authorisation is not None:
            if self._configuration.authorisation.classname is not None:
                try:
                    classobject = ClassLoader.instantiate_class(self._configuration.authorisation.classname)
                    self._authorisation = classobject(self._configuration.authorisation)
                    self._authorisation.initialise(client)
                except Exception as excep:
                    YLogger.exception(self, "Failed to instatiate authorisation class", excep)
        else:
            YLogger.debug(self, "No authorisation configuration defined")

    def load_account_linking_service(self, client):
        if self._configuration.account_linker is not None:
            if self._configuration.account_linker.classname is not None:
                try:
                    classobject = ClassLoader.instantiate_class(self._configuration.account_linker.classname)
                    self._account_linker = classobject(self._configuration.account_linker)
                    self.account_linker.initialise(client)
                except Exception as excep:
                    YLogger.exception(self, "Failed to instatiate authorisation class", excep)
        else:
            YLogger.debug(self, "No authorisation configuration defined")


    def failed_authentication(self, client_context):
        YLogger.error(client_context, "[%s] failed authentication!")

        # If we have an SRAI defined, then use that
        if self.authentication.configuration.denied_srai is not None:
            match_context = client_context.brain.aiml_parser.match_sentence(client_context,
                                                             Sentence(client_context.brain.tokenizer, self.authentication.configuration.denied_srai),
                                                             topic_pattern="*",
                                                             that_pattern="*")
            # If the SRAI matched then return the result
            if match_context is not None:
                return client_context.brain.resolve_matched_template(client_context, match_context)

        # Otherswise return the static text, which is either
        #    User defined via config.yaml
        #    Or use the default value BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED
        return self.authentication.configuration.denied_text

    def authenticate_user(self, client_context):
        if self.authentication is not None:
            if self.authentication.authenticate(client_context) is False:
                return self.failed_authentication(client_context)
        return None

