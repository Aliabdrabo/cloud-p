import uuid
import hashlib
from domain.entities.User import User


from application.interfaces.auth_service import AuthServiceInterface
from infrastructure.repositories.user_repository import InMemoryUserRepository

class SimpleAuthService(AuthServiceInterface):
    def __init__(self, user_repo: InMemoryUserRepository):
        self.user_repo = user_repo

    def register(self, username: str, password: str, role: str):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User(str(uuid.uuid4()), username, password_hash, role)
        self.user_repo.save(user)
        return user

    def login(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if user and user.password_hash == hashlib.sha256(password.encode()).hexdigest():
            return user
        return None
