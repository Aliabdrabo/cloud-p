from abc import ABC, abstractmethod
from domain.entities.delivery import Delivery

class DeliveryRepositoryInterface(ABC):
    @abstractmethod
    def save(self, delivery: Delivery):
        pass

    @abstractmethod
    def get_by_assigned_to(self, user_id: str):
        pass

    @abstractmethod
    def update_status(self, delivery_id: str, status):
        pass

    @abstractmethod
    def get_by_id(self, delivery_id: str):
        pass
