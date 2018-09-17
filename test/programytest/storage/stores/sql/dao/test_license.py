
import unittest

from programy.storage.stores.sql.dao.license import LicenseKey

class LicenseKeyTests(unittest.TestCase):
    
    def test_init(self):
        license1 = LicenseKey(name='license', key="key")
        self.assertIsNotNone(license1)
        self.assertEqual("<LicenseKey(id='n/a', name='license', key='key')>", str(license1))
        
        license = LicenseKey(id=1, name='license', key="key")
        self.assertIsNotNone(license)
        self.assertEqual("<LicenseKey(id='1', name='license', key='key')>", str(license))
