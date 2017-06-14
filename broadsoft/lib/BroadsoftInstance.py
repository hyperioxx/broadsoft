class BroadsoftInstance:
    default_group_id = 'mit'

    def __init__(self, group_id='mit', auth_object=None, login_object=None, session_id=None):
        # these attrs relate to communicating with the Broadsoft API
        self.api_url = '[unknown]'
        self.auth_object = auth_object
        self.auto_logout = True
        self.creds_member = 'prod'
        self.login_object = login_object
        self.session_id = session_id

        # these attrs are inherited by request objects
        self.default_domain = 'broadsoft.mit.edu'
        self.service_provider = 'ENT136'


class TestBroadsoftInstance(BroadsoftInstance):
    def __init__(self, **kwargs):
        BroadsoftInstance.__init__(self, **kwargs)

        # overwrite attrs that are different for test instance
        self.api_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
        self.creds_member = 'test'
        self.default_domain = 'broadsoft-dev.mit.edu'
        self.service_provider = 'ENT136'


def factory(use_test=False) -> object:
    if use_test:
        return TestBroadsoftInstance()

    return BroadsoftInstance()