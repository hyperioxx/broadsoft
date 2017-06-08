class BroadsoftInstance:
    default_group_id = 'mit'

    def __init__(self, group_id=None):
        self.api_url = '[unknown]'
        self.creds_member = 'prod'
        self.default_domain = 'broadsoft.mit.edu'
        self.service_provider = 'ENT136'
        self.group_id = None
        if not self.group_id:
            self.group_id = self.default_group_id


class TestBroadsoftInstance(BroadsoftInstance):
    def __init__(self, **kwargs):
        BroadsoftInstance.__init__(self, **kwargs)
        self.api_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
        self.creds_member = 'test'
        self.default_domain = 'broadsoft-dev.mit.edu'


def factory(use_test=False):
    if use_test:
        return TestBroadsoftInstance()

    return BroadsoftInstance()