class User:
    def __init__(self, user_id: str, username: str, password_hash: str, role: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role


    def is_merchant(self):
        return self.role == 'merchant'

    def is_delivery_person(self):
        return self.role == 'delivery'



