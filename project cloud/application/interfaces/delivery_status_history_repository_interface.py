from abc import ABC, abstractmethod

class DeliveryStatusHistoryRepositoryInterface(ABC):
    @abstractmethod
    def log_status_change(self, delivery_id: str, status: str):
        pass