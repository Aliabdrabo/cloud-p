from application.interfaces.delivery_status_history_repository_interface import DeliveryStatusHistoryRepositoryInterface

class InMemoryDeliveryStatusHistoryRepository(DeliveryStatusHistoryRepositoryInterface):
    def __init__(self):
        self.history = []

    def log_status_change(self, delivery_id: str, status: str):
        self.history.append({"delivery_id": delivery_id, "status": status})