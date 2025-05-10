class ViewAssignedDeliveries:
    def __init__(self, delivery_service):
        self.delivery_service = delivery_service

    def execute(self, delivery_person_id):
        return self.delivery_service.get_assigned_deliveries(delivery_person_id)
