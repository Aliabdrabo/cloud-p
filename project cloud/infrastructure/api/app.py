import sys
import os
import webbrowser
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS

# Add the app base directory to Python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, BASE_DIR)

# Import application logic
from application.use_cases.login_user import LoginUser
from application.use_cases.register_user import RegisterUser
from application.use_cases.request_delivery import RequestDelivery
from application.use_cases.update_delivery_status import UpdateDeliveryStatus
from application.use_cases.view_assigned_deliveries import ViewAssignedDeliveries
from infrastructure.repositories.user_repository import InMemoryUserRepository
from infrastructure.services.auth_service import SimpleAuthService
from infrastructure.services.delivery_service import DeliveryService

# Initialize services
user_repo = InMemoryUserRepository()
auth_service = SimpleAuthService(user_repo)
register_user_use_case = RegisterUser(auth_service)
delivery_service = DeliveryService()
request_delivery_use_case = RequestDelivery(delivery_service)
update_delivery_status_use_case = UpdateDeliveryStatus(delivery_service)
view_assigned_deliveries_use_case = ViewAssignedDeliveries(delivery_service)

# Initialize Flask app with the correct template folder path
# Since app.py is in infrastructure/api, and frontend is in the same directory
app = Flask(
    __name__,
    template_folder='frontend',  # Just 'frontend' since it's in the same directory as app.py
    static_folder='frontend'     # Same for static files
)
CORS(app)

# For debugging
print(f"Template folder: {os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend'))}")
print(f"Does it exist? {os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend')))}")
print(f"Files in template folder: {os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend')))}")

# 🏠 Main page
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

# ✅ Register page
@app.route('/register-page')
def register_page():
    return render_template('Register.html')  # Note capital R

# ✅ Login page
@app.route('/login-page')
def login_page():
    return render_template('login.html')

# ✅ Request delivery page
@app.route('/request-delivery')
def request_delivery_page():
    return render_template('request_delivery.html')

# ✅ Assigned deliveries page
@app.route('/assigned-deliveries')
def assigned_deliveries_page():
    return render_template('assigned_deliveries.html')

# ✅ Update delivery status page (both versions)
@app.route('/update-delivery-status')
def update_delivery_status_page():
    # Choose one of these based on which file you want to use
    return render_template('update_delivery_status.html')  

# ✅ Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = register_user_use_case.execute(username, password, role)

    if user:
        return jsonify({"message": "User registered successfully", "user_id": user.user_id}), 201
    return jsonify({"error": "Registration failed"}), 400

# ✅ Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    login_use_case = LoginUser(auth_service)
    user = login_use_case.execute(username, password)

    if user:
        return jsonify({"message": "Login successful", "user_id": user.user_id, "role": user.role}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# ✅ Create delivery
@app.route('/delivery', methods=['POST'])
def create_delivery():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        size = data.get("size")
        weight = data.get("weight")
        address = data.get("address")

        new_delivery = delivery_service.create_delivery(user_id, size, weight, address)
        new_delivery.assign_to("person-1")

        return jsonify({"delivery_id": new_delivery.delivery_id}), 201

    except Exception as e:
        print("❌ Error in /delivery:", e)
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

# ✅ Update status
@app.route('/delivery-status', methods=['PATCH'])
def update_status():
    data = request.json
    delivery_id = data.get('delivery_id')
    new_status = data.get('status')

    if not delivery_id or not new_status:
        return jsonify({"error": "Missing delivery_id or status"}), 400

    success = update_delivery_status_use_case.execute(delivery_id, new_status)
    if success:
        return jsonify({"message": "Delivery status updated"}), 200
    return jsonify({"error": "Failed to update status"}), 400

# ✅ View assigned deliveries
@app.route('/assigned-deliveries/<delivery_person_id>', methods=['GET'])
def assigned_deliveries(delivery_person_id):
    deliveries = view_assigned_deliveries_use_case.execute(delivery_person_id)
    return jsonify([delivery.to_dict() for delivery in deliveries]), 200

# ✅ Assign delivery
@app.route('/assign-delivery', methods=['POST'])
def assign_delivery():
    data = request.get_json()
    delivery_id = data.get("delivery_id")
    user_id = data.get("user_id")

    if not delivery_id or not user_id:
        return jsonify({"error": "Missing delivery_id or user_id"}), 400

    success = delivery_service.assign_delivery_to_person(delivery_id, user_id)

    if success:
        return jsonify({"message": f"Assigned delivery {delivery_id} to person {user_id}"}), 200
    return jsonify({"error": "Delivery not found or could not be assigned"}), 404

# Run the app
if __name__ == '__main__':
    print("Running from:", os.getcwd())
    print("sys.path:", sys.path)
    
    # Open browser automatically when starting the server
    webbrowser.open('http://127.0.0.1:5000/')
    
    app.run(host='0.0.0.0', port=5000, debug=True)