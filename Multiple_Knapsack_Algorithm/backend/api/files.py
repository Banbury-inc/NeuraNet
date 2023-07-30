from flask import jsonify, request, Blueprint

files_bp = Blueprint("files", __name__)

# Sample data (in real-world, this would come from a database)
files = [
    {"id": 1, "name": "File 1", "size": 50, "priority": 3},
    {"id": 2, "name": "File 2", "size": 30, "priority": 2},
    # Add more files here
]

@files_bp.route("/files", methods=["GET"])
def get_files():
    return jsonify(files)

# Additional API endpoints for adding, updating, and deleting files
