from domain.entities.delivery import Delivery
from domain.entities.package import Package
from domain.enums.delivery_status import DeliveryStatus

class RequestDelivery:
    def __init__(self, delivery_service):
        self.delivery_service = delivery_service

    def execute(self, user_id, size, weight, address):
        return self.delivery_service.create_delivery(user_id, size, weight, address)
