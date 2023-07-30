from flask import jsonify, request, Blueprint

devices_bp = Blueprint("devices", __name__)

# Sample data (in real-world, this would come from a database)
devices = [
    {"id": 1, "name": "Device 1", "storage_capacity": 100},
    {"id": 2, "name": "Device 2", "storage_capacity": 200},
    # Add more devices here
]

@devices_bp.route("/devices", methods=["GET"])
def get_devices():
    return jsonify(devices)

# Additional API endpoints for adding, updating, and deleting devices
