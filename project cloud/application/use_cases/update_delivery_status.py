from domain.enums.delivery_status import DeliveryStatus

class UpdateDeliveryStatus:
    def __init__(self, delivery_service):
        self.delivery_service = delivery_service

    def execute(self, delivery_id, new_status_str):
        try:
            # طباعة البيانات المدخلة للتحقق
            print(f"Attempting to update delivery status: {delivery_id}, New Status: {new_status_str}")
            
            # تحويل النص إلى Enum باستخدام الاسم (name) وليس القيمة (value)
            new_status = DeliveryStatus[new_status_str.upper()]
            
            # التحقق من نجاح التحديث
            success = self.delivery_service.update_status(delivery_id, new_status)
            if success:
                print(f"Status updated successfully for delivery_id: {delivery_id}")
            else:
                print(f"Failed to update status for delivery_id: {delivery_id}")
            return success
            
        except KeyError:
            print(f"Invalid status name: {new_status_str}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
