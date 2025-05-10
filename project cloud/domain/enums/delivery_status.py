from enum import Enum

class DeliveryStatus(Enum):
    REQUESTED = "Requested"
    PICKED_UP = "Picked Up"
    DELIVERED = "Delivered"
