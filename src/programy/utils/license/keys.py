import logging

class LicenseKeys(object):

    def __init__(self):
        self._keys = {}

    def has_key(self, name):
        return bool(name in self._keys)

    def get_key(self, name):
        if name in self._keys:
            return self._keys[name]
        else:
            raise ValueError("No license key named [%s]"%name)

    def load_license_key_data(self, license_key_data):
        lines = license_key_data.split('\n')
        for line in lines:
            self._process_license_key_line(line)

    def load_license_key_file(self, license_key_filename):
        try:
            with open(license_key_filename, "r+") as license_file:
                for line in license_file:
                    self._process_license_key_line(line)
        except:
            logging.error("Invalid license key file [%s]"%license_key_filename)

    def _process_license_key_line(self, line):
        line = line.strip()
        if len(line)> 0:
            if line.startswith('#') is False:
                splits = line.split("=")
                if len(splits) == 2:
                    key_name = splits[0].strip()
                    key = splits[1].strip()
                    self._keys[key_name] = key
                else:
                    logging.warning ("Invalid license key [%s]"%line)
