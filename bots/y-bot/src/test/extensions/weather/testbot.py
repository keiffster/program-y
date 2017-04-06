from programy.utils.license.keys import LicenseKeys

class TestBrain(object):

    def __init__(self):
        self._license_keys = LicenseKeys()

    @property
    def license_keys(self):
        return self._license_keys

class TestBot(object):

    def __init__(self):
        self._brain = TestBrain()

    @property
    def brain(self):
        return self._brain
