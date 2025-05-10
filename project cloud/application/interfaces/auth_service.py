from abc import ABC, abstractmethod

class AuthServiceInterface(ABC):
    @abstractmethod
    def register(self, username: str, password: str, role: str):
        pass

    @abstractmethod
    def login(self, username: str, password: str):
        pass
