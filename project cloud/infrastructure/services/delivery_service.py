import uuid
from flask import Flask, request, jsonify

class Delivery:
    def __init__(self, user_id, size, weight, address):
        self.delivery_id = str(uuid.uuid4())  # إنشاء UUID فريد
        self.user_id = user_id
        self.size = size
        self.weight = weight
        self.address = address
        self.status = None  # الحالة الأولية
        self.assigned_to = None  # المندوب المعين

    def __str__(self):
        return f"Delivery ID: {self.delivery_id}, Status: {self.status}, Assigned To: {self.assigned_to}"

    def assign_to(self, person_id):
        self.assigned_to = person_id  # تعيين المندوب
        print(f"Assigned delivery {self.delivery_id} to person {self.assigned_to}")

    def to_dict(self):
        # التأكد من أن دالة to_dict تقوم بإرجاع قيم كافة الخصائص
        return {
            "delivery_id": self.delivery_id,
            "size": self.size,
            "weight": self.weight,
            "address": self.address,
            "status": self.status,
            "assigned_to": self.assigned_to  # إضافة الحقل الخاص بالمندوب
        }


class DeliveryService:
    def __init__(self):
        self.deliveries = []  # قائمة لتخزين جميع التسليمات

    def create_delivery(self, user_id, size, weight, address):
        # إنشاء تسليم جديد
        delivery = Delivery(user_id, size, weight, address)
        self.deliveries.append(delivery)  # إضافة التسليم إلى القائمة
        print(f"Created delivery with ID: {delivery.delivery_id}")  # طباعة الـ delivery_id عند الإنشاء
        return delivery

    def get_delivery_by_id(self, delivery_id):
        for delivery in self.deliveries:
            if delivery.delivery_id == delivery_id:
                return delivery
        return None  # إذا لم يتم العثور على التسليم

    def assign_delivery_to_person(self, delivery_id, person_id):
        # البحث عن التسليم وتخصيصه للمندوب
        delivery = self.get_delivery_by_id(delivery_id)
        if delivery:
            delivery.assign_to(person_id)
            return True
        return False  # إذا لم يتم العثور على التسليم

    def get_assigned_deliveries(self, delivery_person_id):
        # إرجاع التسليمات التي تم تعيينها للمندوب
        assigned_deliveries = [delivery for delivery in self.deliveries if delivery.assigned_to == delivery_person_id]
        return assigned_deliveries

    def update_status(self, delivery_id, new_status):
        # البحث عن التسليم وتحديث حالته
        delivery = self.get_delivery_by_id(delivery_id)
        if delivery:
            delivery.status = new_status
            print(f"Updated delivery {delivery_id} status to {new_status}")
            return True
        return False  # إذا لم يتم العثور على التسليم


# إعداد الـ Flask API
delivery_service = DeliveryService()

app = Flask(__name__)

# ✅ Create Delivery Request
@app.route('/delivery', methods=['POST'])
def create_delivery():
    data = request.get_json()
    user_id = data.get("user_id")
    size = data.get("size")
    weight = data.get("weight")
    address = data.get("address")

    # إنشاء التسليم
    new_delivery = delivery_service.create_delivery(user_id, size, weight, address)
    
    return jsonify({"delivery_id": new_delivery.delivery_id}), 201

# ✅ Assign Delivery to a Person
@app.route('/assign-delivery', methods=['POST'])
def assign_delivery():
    data = request.get_json()
    delivery_id = data.get("delivery_id")
    person_id = data.get("person_id")

    # تخصيص المندوب للتسليم
    success = delivery_service.assign_delivery_to_person(delivery_id, person_id)
    if success:
        return jsonify({"message": f"Assigned delivery {delivery_id} to person {person_id}"}), 200
    else:
        return jsonify({"error": "Delivery not found"}), 404

# ✅ View Assigned Deliveries
@app.route('/assigned-deliveries/<delivery_person_id>', methods=['GET'])
def assigned_deliveries(delivery_person_id):
    # إرجاع التسليمات المعينة للمندوب باستخدام دالة get_assigned_deliveries
    deliveries = delivery_service.get_assigned_deliveries(delivery_person_id)
    return jsonify([{
        "delivery_id": delivery.delivery_id,
        "size": delivery.size,
        "weight": delivery.weight,
        "address": delivery.address,
        "status": delivery.status
    } for delivery in deliveries]), 200

# ✅ Update Delivery Status
@app.route('/delivery-status', methods=['PATCH'])
def update_status():
    data = request.json
    delivery_id = data.get('delivery_id')
    new_status = data.get('status')

    if not delivery_id or not new_status:
        return jsonify({"error": "Missing delivery_id or status"}), 400

    print(f"Received delivery_id: {delivery_id}, status: {new_status}")

    # تحديث الحالة باستخدام دالة update_status من DeliveryService
    success = delivery_service.update_status(delivery_id, new_status)
    if success:
        return jsonify({"message": "Delivery status updated"}), 200
    return jsonify({"error": "Failed to update status"}), 400

if __name__ == "__main__":
    app.run(debug=True)
