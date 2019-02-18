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

from programy.config.section import BaseSectionConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BrainSecurityConfiguration(BaseSectionConfigurationData):

    DEFAULT_ACCESS_DENIED = "Access denied!"

    def __init__(self, service_name):
        BaseSectionConfigurationData.__init__(self, service_name)
        self._classname = None
        self._denied_srai = None
        self._denied_text = None

    @property
    def classname(self):
        return self._classname

    @property
    def denied_srai(self):
        return self._denied_srai

    @property
    def denied_text(self):
        return self._denied_text

    def check_for_license_keys(self, license_keys):
        BaseSectionConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        service = configuration_file.get_section(self.section_name, configuration)
        if service is not None:
            self._classname = configuration_file.get_option(service, "classname", missing_value=None, subs=subs)
            self._denied_srai = configuration_file.get_option(service, "denied_srai", missing_value=None, subs=subs)
            self._denied_text = configuration_file.get_option(service, "denied_text",
                                                              missing_value=BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED, subs=subs)
        else:
            YLogger.warning(self, "'security' section missing from bot config, using to defaults")


class BrainSecurityAuthenticationConfiguration(BrainSecurityConfiguration):

    def __init__(self, service_name="authentication"):
        BrainSecurityConfiguration.__init__(self, service_name)
        self._classname =  "programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService"
        self._denied_srai = "AUTHENTICATION_FAILED"
        self._denied_text = "Access Denied!"

    def check_for_license_keys(self, license_keys):
        BrainSecurityConfiguration.check_for_license_keys(self, license_keys)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = "programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService"
            data['denied_srai'] = "AUTHENTICATION_FAILED"
            data['denied_text'] = "Access Denied!"
        else:
            data['classname'] = self._classname
            data['denied_srai'] = self._denied_srai
            data['denied_text'] = self._denied_text


class BrainSecurityAuthorisationConfiguration(BrainSecurityConfiguration):

    def __init__(self, service_name="authorisation"):
        BrainSecurityConfiguration.__init__(self, service_name)
        self._classname = "programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService"
        self._denied_srai = "AUTHORISATION_FAILED"
        self._denied_text = "Access Denied!"

    def check_for_license_keys(self, license_keys):
        BrainSecurityConfiguration.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        super(BrainSecurityAuthorisationConfiguration, self).load_config_section(configuration_file, configuration, bot_root, subs=subs)
        service = configuration_file.get_section(self.section_name, configuration)
        self.load_additional_key_values(configuration_file, service)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = "programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService"
            data['denied_srai'] = "AUTHORISATION_FAILED"
            data['denied_text'] = "Access Denied!"
        else:
            data['classname'] = self._classname
            data['denied_srai'] = self._denied_srai
            data['denied_text'] = self._denied_text


class BrainSecurityAccountLinkerConfiguration(BrainSecurityConfiguration):

    def __init__(self, service_name="account_linker"):
        BrainSecurityConfiguration.__init__(self, service_name)
        self._classname = "programy.security.linking.accountlinker.BasicAccountLinkerService"
        self._denied_srai = "ACCOUNT_LINKING_FAILED"
        self._denied_text = "Unable to link accounts!"

    def check_for_license_keys(self, license_keys):
        BrainSecurityConfiguration.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        super(BrainSecurityAccountLinkerConfiguration, self).load_config_section(configuration_file, configuration, bot_root, subs=subs)
        service = configuration_file.get_section(self.section_name, configuration)
        self.load_additional_key_values(configuration_file, service)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = "programy.security.linking.accountlinker.BasicAccountLinkerService"
            data['denied_srai'] = "ACCOUNT_LINKING_FAILED"
            data['denied_text'] = "Unable to link accounts!"
        else:
            data['classname'] = self._classname
            data['denied_srai'] = self._denied_srai
            data['denied_text'] = self._denied_text

