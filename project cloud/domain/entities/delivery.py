import uuid
from domain.enums.delivery_status import DeliveryStatus
from domain.entities.package import Package

class Delivery:
    def __init__(self, merchant_id, package: Package, status=DeliveryStatus.REQUESTED, assigned_to=None):
        self.delivery_id = str(uuid.uuid4())  # توليد معرف فريد عند إنشاء الكائن
        self.merchant_id = merchant_id
        self.package = package
        self.status = status
        self.assigned_to = assigned_to  # ID الخاص بشخص التوصيل إذا كان تم تعيينه

    def assign_delivery_person(self, delivery_person_id):
        self.assigned_to = delivery_person_id

    def update_status(self, new_status: DeliveryStatus):
        allowed_transitions = {
            DeliveryStatus.REQUESTED: [DeliveryStatus.PICKED_UP],
            DeliveryStatus.PICKED_UP: [DeliveryStatus.DELIVERED],
            DeliveryStatus.DELIVERED: []
        }
        if new_status in allowed_transitions[self.status]:
            self.status = new_status
        else:
            raise ValueError(f"Cannot change status from {self.status} to {new_status}")

    def to_dict(self):
        return {
            "delivery_id": self.delivery_id,
            "merchant_id": self.merchant_id,
            "package": self.package.to_dict(),  # Assuming package has a to_dict method
            "status": self.status.name,  # Assuming status is an enum, convert to string
            "assigned_to": self.assigned_to
        }


