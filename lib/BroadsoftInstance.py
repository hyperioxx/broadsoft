class BroadsoftInstance:
    default_group_id = 'mit'

    def __init__(self, group_id=None, auth_object=None, login_object=None, session_id=None):
        self.api_url = '[unknown]'
        self.auth_object = auth_object
        self.auto_logout = True
        self.creds_member = 'prod'
        self.default_domain = 'broadsoft.mit.edu'
        self.login_object = login_object
        self.service_provider = 'ENT136'
        self.session_id = session_id
        self.group_id = None
        if not self.group_id:
            self.group_id = self.default_group_id


class TestBroadsoftInstance(BroadsoftInstance):
    def __init__(self, **kwargs):
        BroadsoftInstance.__init__(self, **kwargs)
        self.api_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
        self.creds_member = 'test'
        self.default_domain = 'broadsoft-dev.mit.edu'


def factory(use_test=False) -> object:
    if use_test:
        return TestBroadsoftInstance()

    return BroadsoftInstance()