from abc import ABC, abstractmethod
from domain.entities.User import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def get_by_username(self, username: str):
        pass
