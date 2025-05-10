from domain.entities.delivery import Delivery
from application.interfaces.delivery_repository_interface import DeliveryRepositoryInterface

class InMemoryDeliveryRepository(DeliveryRepositoryInterface):
    def __init__(self):
        self.deliveries = {}

    def save(self, delivery: Delivery):
        self.deliveries[delivery.delivery_id] = delivery

    def get_by_assigned_to(self, user_id: str):
        return [d for d in self.deliveries.values() if d.assigned_to == user_id]

    def update_status(self, delivery_id: str, status):
        if delivery_id in self.deliveries:
            self.deliveries[delivery_id].status = status

    def get_by_id(self, delivery_id: str):
        return self.deliveries.get(delivery_id)