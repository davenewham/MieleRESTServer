

class MieleRESTException (Exception):
    def __init__ (self, error, device):
        self.device = device;
        self.error=error;
    def asdict (self):
        return {'error': self.error, 'device':self.device};
