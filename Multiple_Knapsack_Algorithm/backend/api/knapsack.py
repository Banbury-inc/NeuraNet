from flask import jsonify, request, Blueprint
from algorithms.knapsack import multiple_knapsack

knapsack_bp = Blueprint("knapsack", __name__)

@knapsack_bp.route("/knapsack", methods=["POST"])
def solve_knapsack():
    data = request.get_json()
    files = data["files"]
    devices = data["devices"]

    # Call the multiple_knapsack function from the algorithms module
    total_storage, allocation_strategy = multiple_knapsack(files, devices)

    response = {
        "total_storage": total_storage,
        "allocation_strategy": allocation_strategy
    }
    return jsonify(response)
