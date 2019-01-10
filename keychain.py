import json

from workflow import PasswordNotFound


class AuthKeys(dict):

    keychain_account = '2fa_keys'

    def __init__(self, workflow, **kwargs):
        super(AuthKeys, self).__init__(**kwargs)
        self._wf = workflow
        self._load()

    def _load(self):
        try:
            json_data = self._wf.get_password(self.keychain_account)
        except PasswordNotFound:
            self._wf.logger.info('No data found in keychain')
            return

        data = json.loads(json_data)
        for key, value in data.iteritems():
            self[key] = value

    def save(self):
        json_data = json.dumps(self)
        self._wf.save_password(self.keychain_account, json_data)
