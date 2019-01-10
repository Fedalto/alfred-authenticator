import json
import sys
import unittest
from StringIO import StringIO

import pyotp
from authenticator import add_new_service, list_tokens
from workflow import Workflow3


class DummyKeyChain(dict):
    def save(self):
        pass


class AuthenticatorTestCase(unittest.TestCase):
    def setUp(self):
        self.wf = Workflow3()
        self.keychain = DummyKeyChain()
        self._stdout = StringIO()
        self._original_stdout = sys.stdout
        sys.stdout = self._stdout

    @property
    def wf_output(self):
        return json.loads(self._stdout.getvalue())

    def tearDown(self):
        sys.stdout = self._original_stdout

    def test_add_new_service(self):
        add_new_service(self.keychain, self.wf, "test_service", "R7E4TPLEKX5ZO54N")

        self.assertIn("test_service", self.keychain)
        self.assertEqual(self.keychain["test_service"], "R7E4TPLEKX5ZO54N")

        list_tokens(self.keychain, self.wf)

        self.assertEqual(len(self.wf_output['items']), 1)
        self.assertEqual(self.wf_output['items'][0]['title'], 'test_service')
        token = self.wf_output['items'][0]['subtitle']
        self.assertEqual(len(token), 6)

    def test_not_overwrite_service(self):
        add_new_service(self.keychain, self.wf, "test_service", "R7E4TPLEKX5ZO54N")
        with self.assertRaisesRegexp(ValueError, 'Duplicate service name'):
            new_secret = pyotp.random_base32()
            add_new_service(self.keychain, self.wf, "test_service", new_secret)


if __name__ == '__main__':
    unittest.main()
