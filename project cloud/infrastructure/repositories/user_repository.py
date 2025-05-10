import uuid
from domain.entities.User import User
from application.interfaces.user_repository_interface import UserRepositoryInterface

class InMemoryUserRepository(UserRepositoryInterface):
    def __init__(self):
        self.users = {}

    def save(self, user: User):
        self.users[user.username] = user

    def get_by_username(self, username: str):
        return self.users.get(username)
