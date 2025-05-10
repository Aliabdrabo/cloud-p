class LoginUser:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def execute(self, username, password):
        return self.auth_service.login(username, password)