class ValidationError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

class LoginError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
