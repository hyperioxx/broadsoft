class BroadsoftObject:
    def provision(self):
        ro = self.build_request_object()
        results = ro.post()
        return results