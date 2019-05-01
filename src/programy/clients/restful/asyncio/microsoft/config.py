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
from programy.clients.restful.config import RestConfiguration
from programy.utils.substitutions.substitues import Substitutions


class MicrosoftConfiguration(RestConfiguration):

    NEW_USER_TEXT = "Hello and welcome, I'm here to help."

    def __init__(self):
        RestConfiguration.__init__(self, "microsoft")
        self._new_user_text = MicrosoftConfiguration.NEW_USER_TEXT
        self._new_user_srai = None

    @property
    def new_user_text(self):
        return self._new_user_text
    @property
    def new_user_srai(self):
        return self._new_user_srai

    def check_for_license_keys(self, license_keys):
        RestConfiguration.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, microsoft, bot_root, subs: Substitutions = None):
        if microsoft is not None:
            self._new_user_text = configuration_file.get_option(microsoft, "new_user_text", missing_value=MicrosoftConfiguration.NEW_USER_TEXT, subs=subs)
            self._new_user_srai = configuration_file.get_option(microsoft, "new_user_srai", missing_value=None, subs=subs)
            super(MicrosoftConfiguration, self).load_configuration_section(configuration_file, microsoft, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["new_user_text"] = MicrosoftConfiguration.NEW_USER_TEXT
            data["new_user_srai"] = None
        else:
            data["new_user_text"] = self._new_user_text
            data["new_user_srai"] = self._new_user_srai

        super(MicrosoftConfiguration, self).to_yaml(data, defaults)
